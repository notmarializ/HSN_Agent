import pandas as pd
import tempfile
import os
from google.cloud import storage
from fuzzywuzzy import process
from models.hsn_code import HsnCode
from typing import Optional

class HSNDataService:
    def __init__(self, gcs_path, sheet_name):
        self.sheet_name = sheet_name
        self.client = storage.Client()
        self.temp_file_path = None
        self.df = self._load_data_from_gcs(gcs_path)
        self._build_indexes()

    def _load_data_from_gcs(self, gcs_path):
        try:
            # Create a temporary file with explicit cleanup
            temp_file = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False)
            self.temp_file_path = temp_file.name
            temp_file.close()  # Close immediately so we can use it
            
            bucket_name, blob_name = gcs_path.split('/', 1)
            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            blob.download_to_filename(self.temp_file_path)
            
            # Load the Excel file
            df = pd.read_excel(self.temp_file_path, sheet_name=self.sheet_name)
            
            # Clean column names
            df.columns = [col.strip() for col in df.columns]
            
            print("Columns in sheet:", df.columns.tolist())
            return df
        except Exception as e:
            self._cleanup_temp_file()
            raise

    def _build_indexes(self):
        """Build indexes with proper column name handling"""
        hsn_column = next(col for col in self.df.columns if 'HSNCode' in col)
        desc_column = 'Description'
        
        self.df[hsn_column] = self.df[hsn_column].astype(str).str.strip()
        self.df = self.df.dropna(subset=[hsn_column])
        
        self.code_index = {
            row[hsn_column]: row[desc_column] 
            for _, row in self.df.iterrows()
        }

        self.hierarchy_index = {}
        for code in self.code_index.keys():
            code = str(code).strip()
            for length in [2, 4, 6]:
                if len(code) > length:
                    parent = code[:length]
                    if parent not in self.hierarchy_index:
                        self.hierarchy_index[parent] = self.code_index.get(parent, None)
        
        # Clean up temp file now that we're done with it
        self._cleanup_temp_file()

    def _cleanup_temp_file(self):
        """Safely remove the temporary file if it exists"""
        if self.temp_file_path and os.path.exists(self.temp_file_path):
            try:
                os.unlink(self.temp_file_path)
            except Exception as e:
                print(f"Warning: Could not delete temp file {self.temp_file_path}: {str(e)}")
            finally:
                self.temp_file_path = None

    def __del__(self):
        """Destructor to ensure cleanup"""
        self._cleanup_temp_file()

    def get(self, code: str) -> Optional[HsnCode]:
        row = self.df[self.df['HSNCode'] == code]
        if not row.empty:
            return HsnCode(
                code=row.iloc[0]['HSNCode'],
                description=row.iloc[0]['Description']
            )
        return None


    def get_by_code(self, code):
        return self.code_index.get(str(code).strip(), None)

    def search(self, query, limit=5):
        if not query:
            return []

        results = process.extract(
            query, 
            self.df['Description'].dropna().tolist(), 
            limit=limit
        )
        
        return [
            {
                'code': str(row['HSNCode']).strip(),
                'description': desc,
                'confidence': score
            }
            for desc, score, *_ in results
            for _, row in self.df[self.df['Description'] == desc].iterrows()
            if score > 60
        ]
    def get_parents(self, code: str) -> list:
        """Return parent HSN codes based on code length (simple placeholder logic)"""
        if len(code) == 2:
            return []  # No parent for 2-digit codes
        elif len(code) > 2:
            return [code[:2]]  # 01XX → parent is 01
        return []
