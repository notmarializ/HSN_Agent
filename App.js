import React, { useState } from 'react';
import styled, { keyframes } from 'styled-components';

const App = () => {
  const [hsnCode, setHsnCode] = useState('');
  const [description, setDescription] = useState('');
  const [responseText, setResponseText] = useState('');
  const [suggestions, setSuggestions] = useState([]);

  const handleValidate = async () => {
    const payload = {
      queryResult: {
        intent: { displayName: 'ValidateHSNCode' },
        parameters: { hsn_code: hsnCode }
      }
    };
    const res = await fetch('http://localhost:5000/webhook', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    setSuggestions([]);
    setResponseText(data.fulfillmentText);
  };

  const handleSuggest = async () => {
    const payload = {
      queryResult: {
        intent: { displayName: 'SuggestHSNCode' },
        parameters: { description }
      }
    };
    const res = await fetch('http://localhost:5000/webhook', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();

    // deduplicate payload by code + description
    const uniqueSuggestions = Array.from(
      new Map(
        (data.payload || []).map(item => [`${item.code}-${item.description}`, item])
      ).values()
    );

    setResponseText(data.fulfillmentText);
    setSuggestions(uniqueSuggestions);
  };

  return (
    <Container>
      <Title>🔍 HSN Code Validator</Title>

      <InputGroup>
        <Input
          type="text"
          placeholder="Enter HSN Code"
          value={hsnCode}
          onChange={(e) => setHsnCode(e.target.value)}
        />
        <Button onClick={handleValidate}>✅ Validate</Button>
      </InputGroup>

      <InputGroup>
        <Input
          type="text"
          placeholder="Enter Product Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <Button onClick={handleSuggest}>💡 Suggest</Button>
      </InputGroup>

      {(responseText || suggestions.length > 0) && (
        <ResponseBox>
          {suggestions.length > 0 ? (
            <>
              <ResponseHeader>{responseText.split(':')[0]}:</ResponseHeader>
              <SuggestionsList>
                {suggestions.map((s, i) => (
                  <SuggestionItem key={i} confidence={s.confidence}>
                    <Code>{s.code}</Code>
                    <Description>{s.description}</Description>
                    <Confidence value={s.confidence}>
                      Confidence: {s.confidence}%
                    </Confidence>
                  </SuggestionItem>
                ))}
              </SuggestionsList>
            </>
          ) : (
            <SuggestionItem confidence={100}>
              <Description>{responseText}</Description>
            </SuggestionItem>
          )}
        </ResponseBox>
      )}
    </Container>
  );
};

export default App;

// === STYLED COMPONENTS ===

const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
`;

const Container = styled.div`
  max-width: 800px;
  margin: 40px auto;
  padding: 2rem;
  font-family: 'Segoe UI', sans-serif;
`;

const Title = styled.h1`
  text-align: center;
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #2c3e50;
`;

const InputGroup = styled.div`
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
`;

const Input = styled.input`
  flex: 1;
  padding: 0.75rem;
  font-size: 1rem;
  border-radius: 8px;
  border: 1px solid #ccc;
`;

const Button = styled.button`
  padding: 0.75rem 1.5rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
`;

const ResponseBox = styled.div`
  margin-top: 2.5rem;
  animation: ${fadeIn} 0.5s ease-out;
`;

const ResponseHeader = styled.div`
  font-size: 1.1rem;
  font-weight: 600;
  color: #2D3748;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const SuggestionsList = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
`;

const SuggestionItem = styled.div`
  padding: 1rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  border-left: 4px solid ${props =>
    props.confidence > 85 ? '#48BB78' :
    props.confidence > 70 ? '#4299E1' : '#ECC94B'};
`;

const Code = styled.div`
  font-weight: 600;
  color: #2D3748;
  font-size: 1.1rem;
  margin-bottom: 0.25rem;
`;

const Description = styled.div`
  color: #4A5568;
  margin-bottom: 0.5rem;
`;

const Confidence = styled.div`
  font-size: 0.85rem;
  color: ${props =>
    props.value > 85 ? '#48BB78' :
    props.value > 70 ? '#4299E1' : '#D69E2E'};
  font-weight: 500;
`;
