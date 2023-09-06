import { DataGrid, useGridApiContext } from "@mui/x-data-grid";
import axios from "axios";
import { useState, useEffect } from "react";
import settings from "../config/settings.json";
import { Rating, Box } from "@mui/material";
import ToolBar from "./ToolBar";

const columns = [
  { field: "id", headerName: "Id", minWidth: 230 },
  { field: "title", headerName: "Title", minWidth: 395 },
  {
    field: "rating",
    headerName: "Rating",
    editable: true,
    renderCell: (params) => {
      return <Rating value={params.value} readOnly />;
    },
    renderEditCell: function RatingEditCell(props) {
      const { id, value, field } = props;
      const apiRef = useGridApiContext();

      const handleChange = async (_, newValue) => {
        await axios.patch(`${settings.apiUrl}/songs/editRating`, {
          id: id,
          newRating: newValue,
        });
        apiRef.current.setEditCellValue({ id, field, value: newValue });
      };

      return <Rating value={value} onChange={handleChange} />;
    },

    minWidth: 140,
  },
  { field: "danceability", headerName: "Danceability" },
  { field: "energy", headerName: "Energy" },
  { field: "mode", headerName: "Mode" },
  { field: "acousticness", headerName: "Acousticness" },
  { field: "tempo", headerName: "Tempo" },
  { field: "duration_ms", headerName: "Duration (ms)" },
  { field: "num_sections", headerName: "Num Sections" },
  { field: "num_segments", headerName: "Num Segments" },
];

const Table = () => {
  const [dataTableRows, setDataTableRows] = useState([]);
  const [totalRowCount, setTotalRowCount] = useState(0);
  const [pageNumber, setPageNumber] = useState(0);
  const [columnToSort, setColumnToSort] = useState("");
  const [sortingDirection, setSortingDirection] = useState("");

  useEffect(() => {
    async function fetchSongs() {
      const { songs, totalSongs } = await getSongs({ page: 0 });

      setDataTableRows(songs);
      setTotalRowCount(totalSongs);
    }
    fetchSongs();
  }, []);

  async function getSongs({ page, column, direction }) {
    const { data } = await axios.get(`${settings.apiUrl}/songs`, {
      params: {
        page: page ?? pageNumber,
        column: column || columnToSort,
        direction: direction || sortingDirection,
      },
    });

    return data;
  }

  const handlePagination = async ({ page }) => {
    setPageNumber(page);

    const { songs, totalSongs } = await getSongs({ page });

    setDataTableRows(songs);
    setTotalRowCount(totalSongs);
  };

  const handleSorting = async (params) => {
    if (params.length < 1) {
      setColumnToSort("");
      setSortingDirection("");
      return;
    }

    const [{ field, sort }] = params;

    setColumnToSort(field);
    setSortingDirection(sort);

    const { songs, totalSongs } = await getSongs({
      column: field,
      direction: sort,
    });

    setDataTableRows(songs);
    setTotalRowCount(totalSongs);
  };

  return (
    <Box data-testid="mock-datagrid">
      <DataGrid
        disableColumnFilter
        disableColumnSelector
        disableDensitySelector
        rows={dataTableRows}
        columns={columns}
        initialState={{
          pagination: {
            paginationModel: { pageSize: 10, page: 0 },
          },
        }}
        rowCount={totalRowCount}
        paginationMode="server"
        sortingMode="server"
        pageSizeOptions={[10]}
        onPaginationModelChange={handlePagination}
        onSortModelChange={handleSorting}
        slots={{ toolbar: ToolBar }}
        slotProps={{ toolbar: { setDataTableRows, setTotalRowCount } }}
      />
    </Box>
  );
};

export default Table;
