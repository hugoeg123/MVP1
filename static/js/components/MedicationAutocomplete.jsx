import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import debounce from 'lodash.debounce';

const MedicationAutocomplete = ({ endpoint, initialSelected = [], onUpdate, placeholder }) => {
  const [inputValue, setInputValue] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [selectedItems, setSelectedItems] = useState(initialSelected);
  const inputRef = useRef(null);

  const fetchSuggestions = debounce(async (searchTerm) => {
    if (searchTerm.length < 2) {
      setSuggestions([]);
      return;
    }
    try {
      const response = await axios.get(endpoint, { params: { q: searchTerm } });
      setSuggestions(response.data.results);
    } catch (error) {
      console.error('Error fetching suggestions:', error);
    }
  }, 300);

  useEffect(() => {
    fetchSuggestions(inputValue);
    return () => fetchSuggestions.cancel();
  }, [inputValue]);

  const handleSelect = (item) => {
    if (!selectedItems.some(selected => selected.id === item.id)) {
      const newSelected = [...selectedItems, item];
      setSelectedItems(newSelected);
      onUpdate(newSelected);
    }
    setInputValue('');
    setSuggestions([]);
    inputRef.current.focus();
  };

  const removeItem = (itemId) => {
    const newSelected = selectedItems.filter(item => item.id !== itemId);
    setSelectedItems(newSelected);
    onUpdate(newSelected);
  };

  return (
    <div className="autocomplete-section">
      <div className="input-container">
        <input
          ref={inputRef}
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && suggestions[0] && handleSelect(suggestions[0])}
          placeholder={placeholder}
          className="chrome-input"
        />
        {suggestions.length > 0 && (
          <div className="suggestions-panel">
            {suggestions.map((item) => (
              <div
                key={item.id}
                className="suggestion-item"
                onClick={() => handleSelect(item)}
              >
                <div className="suggestion-name">{item.text}</div>
                <div className="suggestion-details">
                  {item.classe_terapeutica && (
                    <span>{item.classe_terapeutica}</span>
                  )}
                  {item.principio_ativo && (
                    <span> • {item.principio_ativo}</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
      <div className="selected-tags">
        {selectedItems.map((item) => (
          <div key={item.id} className="medication-tag">
            <span>{item.text}</span>
            <button 
              onClick={() => removeItem(item.id)}
              className="tag-remove-btn"
              aria-label="Remove medication"
            >
              ×
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MedicationAutocomplete;