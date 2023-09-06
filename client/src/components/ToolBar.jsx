import { useState, useRef } from "react";
import axios from "axios";
import settings from "../config/settings.json";
import { TextField, Button, Box } from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import FileDownloadIcon from "@mui/icons-material/FileDownload";
import { CSVLink } from "react-csv";

const ExportCsv = () => {
  const [songs, setSongs] = useState([]);
  const csvLink = useRef();

  const handleCsvExport = async () => {
    const { data } = await axios.get(`${settings.apiUrl}/songs/all`);

    setSongs(data);

    setTimeout(() => {
      csvLink.current.link.click();
    });
  };

  return (
    <>
      <Button
        onClick={handleCsvExport}
        startIcon={<FileDownloadIcon />}
        variant="outlined"
        size="large"
      >
        Export
      </Button>
      <CSVLink
        data={songs}
        filename="playlist.csv"
        ref={csvLink}
        target="_blank"
      />
    </>
  );
};

function ToolBar({ setDataTableRows, setTotalRowCount }) {
  const handleSearch = async () => {
    const {
      data: { songs, totalSongs },
    } = await axios.get(`${settings.apiUrl}/songs/search`, {
      params: {
        query: searchQuery.trim(),
      },
    });

    setDataTableRows(songs);
    setTotalRowCount(totalSongs);
  };

  const [searchQuery, setSearchQuery] = useState("");

  return (
    <Box
      sx={{
        p: "10px",
        textAlign: "center",
      }}
    >
      <TextField
        size="small"
        label="Search Songs"
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
      />
      <Button
        onClick={handleSearch}
        variant="outlined"
        size="large"
        startIcon={<SearchIcon />}
        sx={{
          mx: 2,
        }}
      >
        Search
      </Button>
      <ExportCsv />
    </Box>
  );
}

export default ToolBar;
