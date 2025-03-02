import React, { useState } from "react";
import axios from "axios";
import { ClipLoader } from "react-spinners";
import { TextField, Button, Typography, List, ListItem, Paper } from "@mui/material";

function App() {
  // Define state variables
  const [resumeText, setResumeText] = useState("");
  const [analysis, setAnalysis] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      // Send resume text to the backend for analysis
      const analysisResponse = await axios.post("http://127.0.0.1:5000/analyze", {
        resume: resumeText,
      });
      setAnalysis(analysisResponse.data);

      // Get job recommendations based on the analysis
      const recommendationsResponse = await axios.post("http://127.0.0.1:5000/recommend", {
        analysis: analysisResponse.data,
      });
      setRecommendations(recommendationsResponse.data);
    } catch (error) {
      console.error("Error details:", error);
      if (error.response) {
        // The request was made and the server responded with a status code
        console.error("Response data:", error.response.data);
        console.error("Response status:", error.response.status);
        console.error("Response headers:", error.response.headers);
        setError(`Error: ${error.response.data.message || "An error occurred. Please try again."}`);
      } else if (error.request) {
        // The request was made but no response was received
        console.error("No response received:", error.request);
        setError("No response received from the server. Please check your connection.");
      } else {
        // Something happened in setting up the request
        console.error("Request setup error:", error.message);
        setError("An error occurred while setting up the request.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper style={{ padding: "20px", maxWidth: "600px", margin: "auto", marginTop: "50px" }}>
      <Typography variant="h4" align="center" gutterBottom>
        Resume Analyzer
      </Typography>
      <form onSubmit={handleSubmit}>
        <TextField
          fullWidth
          multiline
          rows={6}
          placeholder="Paste your resume here"
          value={resumeText}
          onChange={(e) => setResumeText(e.target.value)}
          variant="outlined"
          margin="normal"
        />
        <Button
          type="submit"
          variant="contained"
          color="primary"
          disabled={loading}
          fullWidth
        >
          {loading ? <ClipLoader size={20} color="#ffffff" /> : "Analyze"}
        </Button>
      </form>

      {/* Display error messages */}
      {error && (
        <Typography variant="body1" style={{ color: "red", marginTop: "10px" }}>
          {error}
        </Typography>
      )}

      {/* Display analysis results */}
      {analysis && (
        <div style={{ marginTop: "20px" }}>
          <Typography variant="h5">Analysis Results</Typography>
          <Typography variant="body1">Skills: {analysis.skills.join(", ")}</Typography>
          <Typography variant="body1">Education: {analysis.education.join(", ")}</Typography>
          <Typography variant="body1">Experience: {analysis.experience.join(", ")}</Typography>
        </div>
      )}

      {/* Display recommended jobs */}
      {recommendations.length > 0 && (
        <div style={{ marginTop: "20px" }}>
          <Typography variant="h5">Recommended Jobs</Typography>
          <List>
            {recommendations.map((job, index) => (
              <ListItem key={index}>{job.title}</ListItem>
            ))}
          </List>
        </div>
      )}
    </Paper>
  );
}

export default App;