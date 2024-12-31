import React from 'react';
import { Box, Paper, Typography, Grid } from '@mui/material';
import { Experiment, LLMResponse } from '../types/types';

interface Props {
  experiments: Experiment[];
}

const ResponseComparison: React.FC<Props> = ({ experiments }) => {
  return (
    <Grid container spacing={2}>
      {experiments.map((exp) => (
        exp.responses.map((response: LLMResponse, idx) => (
          <Grid item xs={12} md={6} key={`${exp.id}-${idx}`}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                {exp.models[idx]}
              </Typography>
              <Box sx={{ mb: 2 }}>
                {response.metrics && (
                  <>
                    <Typography variant="subtitle2" color="text.secondary">
                      Response Time: {response.metrics.responseTime}ms
                    </Typography>
                    <Typography variant="subtitle2" color="text.secondary">
                      Accuracy Score: {response.metrics.accuracy || 0}
                    </Typography>
                    <Typography variant="subtitle2" color="text.secondary">
                      Relevancy Score: {response.metrics.relevancy || 0}
                    </Typography>
                  </>
                )}
              </Box>
              <Typography>{response.response}</Typography>
            </Paper>
          </Grid>
        ))
      ))}
    </Grid>
  );
};

export default ResponseComparison;