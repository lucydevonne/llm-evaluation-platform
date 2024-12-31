import React from 'react';
import { FormGroup, FormControlLabel, Checkbox, Paper, Typography } from '@mui/material';

interface ModelSelectorProps {
  availableModels: string[];
  selectedModels: string[];
  onChange: (models: string[]) => void;
}

const ModelSelector: React.FC<ModelSelectorProps> = ({ 
  availableModels, 
  selectedModels, 
  onChange 
}) => {
  const handleModelToggle = (model: string) => {
    const newSelectedModels = selectedModels.includes(model)
      ? selectedModels.filter(m => m !== model)
      : [...selectedModels, model];
    onChange(newSelectedModels);
  };

  return (
    <Paper sx={{ p: 2, mb: 2 }}>
      <Typography variant="h6" gutterBottom>
        Select Models to Compare
      </Typography>
      <FormGroup row>
        {availableModels.map(model => (
          <FormControlLabel
            key={model}
            control={
              <Checkbox
                checked={selectedModels.includes(model)}
                onChange={() => handleModelToggle(model)}
              />
            }
            label={model}
          />
        ))}
      </FormGroup>
    </Paper>
  );
};

export default ModelSelector; 