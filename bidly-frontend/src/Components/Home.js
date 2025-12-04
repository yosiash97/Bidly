  import React, { useState, useEffect } from "react";
  import Navbar from "./Navbar";
  import Slider from '@mui/material-next/Slider';
  import Box from '@mui/material/Box';
  import axios from "axios";
  import { DataGrid } from '@mui/x-data-grid';
  import TableRow from './TableRow';
  import { Audio } from 'react-loader-spinner'
  import Bid from "./Bid";
  import { Load } from "./Load";
  import { IconButton, Tooltip} from '@mui/material';
  import DeleteIcon from '@mui/icons-material/Delete';
  import FileCopyIcon from '@mui/icons-material/FileCopy';
  import DropdownMenu from './DropdownMenu';

  
  const bidRenderer = (rowData) => {
    let rowElementStatus = rowData.status;

    let color = '';
    let disabled = false;
    if (rowElementStatus == 'OPEN') {
      color = '#556B2F';
    } else if (rowElementStatus == 'CLOSED') {
      color = 'Gray';
      disabled = true;
    } else if (rowElementStatus == 'PENDING') {
      color = 'Gray';
      disabled = true;
    }
    return (
      <Bid disabled={disabled} color={color}></Bid>
    )
  }



  const copyUrl = (url) => {
    console.log('url in copyurl', url);
    navigator.clipboard.writeText(url);
  };

  const renderUrlCell = (params) => {
    const handleCopyClick = () => {
      copyUrl(params.row.url);
    };

    return (
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <Tooltip title="Copy URL">
          <IconButton onClick={handleCopyClick}>
            <FileCopyIcon />
          </IconButton>
        </Tooltip>
        <a href={params.row.url} target="_blank" rel="noopener noreferrer"></a>
      </div>
    );
  };

  const renderBidTypeCell = (params) => {
    const bidTypeHash = {
      'civil_engineering': 'Civil Engineering',
      'construction': 'Construction',
      'structural_engineering': 'Structural Engineering'
    }
    return (
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <a> {bidTypeHash[params.row.bid_type]}</a>
      </div>
    );
  };

  const rowStatusRenderer = (rowData) => {
    let rowElementStatus = rowData.status;

    let color = '';
    if (rowElementStatus == 'OPEN') {
      color = 'GREEN';
    } else if (rowElementStatus == 'CLOSED') {
      color = 'RED';
    } else if (rowElementStatus == 'PENDING') {
      color = 'ORANGE';
    }

    return (
      <span style={{ color }}>
        {rowElementStatus}
      </span>
    );
  }

  const Home = () => {
    const [accessCode, setAccessCode] = useState(""); // State variable to track the access code
    const [authenticated, setAuthenticated] = useState(false); // State variable to track authentication status
  
    const handleAccessCodeChange = (event) => {
        setAccessCode(event.target.value);
    };
    console.log("In Home", process.env.REACT_APP_NODE_ENV)
  
    const authenticate = () => {
        // Compare the entered code with a predefined code (e.g., "1234")
        if (accessCode === "3844") {
            setAuthenticated(true);
        } else {
            alert("Incorrect access code. Please try again.");
        }
    };

    const handleDropdownChange = (value) => {
      setSelectedBidType(value);
    };

    const filterRowDataByBidType = () => {
      if (!selectedBidType) {
        return rowData; // If no bid type is selected, return all rows
      }
      console.log("Selected Bid Type: ", selectedBidType)
      return rowData.filter(row => row.bid_type === selectedBidType);
    };    

    const [selectedBidType, setSelectedBidType] = useState(null); // State variable to store the selected bid type
    const [rowData, setRowData] = useState([]);
    useEffect(() => {
      document.title = "Bidly"; // Set the title when the component mounts
    }, []);

    const [loading, setLoading] = useState(false); // State variable to track loading state
    const [sliderValue, setSliderValue] = useState(10); // State variable to track slider value

    const marks = [
      { value: 0, label: '0 miles' },
      { value: 10, label: '10' },
      { value: 20, label: '20m' },
      { value: 30, label: '30m' },
      { value: 40, label: '40m' },
      { value: 50, label: '50m' },
      { value: 60, label: '60m' },
      { value: 70, label: '70m' },
      { value: 80, label: '80m' },
      { value: 90, label: '90m' },
      { value: 100, label: '100 miles' }
    ];

    const columns = [
      { field: 'id', headerName: 'ID', width: 100 },
      { field: 'city', headerName: 'City', width: 150 },
      { field: 'title', headerName: 'Title', width: 750 },
      { field: 'url', headerName: 'URL', width: 25, renderCell: (params) => renderUrlCell(params) },
      { field: 'bid_type', headerName: 'Bid Type', width: 125, renderCell: (params) => renderBidTypeCell(params) },
      { field: 'delete', headerName: 'X', width: 50, renderCell: (params) => renderDeleteCell(params) }
    ];

    const handleDeleteClick = async(id) => {
      console.log("ID -> ", id)
      console.log("Row Data: ", rowData)
      // This method will send a request to backend (grab BID ID and send back to backend to soft delete)
      let response = null;

      if (process.env.REACT_APP_NODE_ENV === 'local') {
        console.log("In Local", id);
        let response = await axios.post('http://localhost:3001/bids/distance', {
          bidID: id
        });
      }
      
      else if (process.env.REACT_APP_NODE_ENV == 'development') {
        console.log("In Process Env Development")
        let response = await axios.post(`${process.env.REACT_APP_BACKEND_DEV_API_URL}bids/distance`, {
          bidID: id
        });
      }
      else if (process.env.REACT_APP_NODE_ENV == 'production') {
        console.log("In Process Env production")
        let response = await axios.post(`${process.env.REACT_APP_BACKEND_API_URL}bids/distance`, {
          bidID: id
        });
      }
      const updatedRowData = rowData.filter(row => row.id !== id);
      setRowData(updatedRowData);
    }
  
    const renderDeleteCell = (params) => {
      return (
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <Tooltip title="Delete RFP/Bid">
            <IconButton onClick={() => handleDeleteClick(params.row.id)} aria-label="delete" size="small">
              <DeleteIcon fontSize="inherit" />
            </IconButton>
          </Tooltip>
          <a href={params.row.url} target="_blank" rel="noopener noreferrer"></a>
        </div>
      );
    };

    const handleCommit = async (event, newValue) => {
      try {
        setLoading(true); // Set loading to true when the request is sent
        let response = {}
        console.log("process.env.NODE_ENV", process.env.REACT_APP_NODE_ENV)
        if (process.env.REACT_APP_NODE_ENV == 'local') {
          console.log("in local")
          response = await axios.get('http://localhost:3001/task/distance', {
            params: {
              sliderValue: newValue
            }
          });
        }
        else if (process.env.REACT_APP_NODE_ENV == 'development') {
          console.log("in else")
          response = await axios.get(`${process.env.REACT_APP_BACKEND_DEV_API_URL}task/distance`, {
            params: {
              sliderValue: newValue
            }
          });
        }
        else if (process.env.REACT_APP_NODE_ENV === 'production') {
          console.log("In If")
          response = await axios.get(`${process.env.REACT_APP_BACKEND_API_URL}task/distance`, {
            params: {
              sliderValue: newValue
            }
          });
          console.log('Backend API URL:', process.env.REACT_APP_BACKEND_API_URL);
          console.log("full: ", `${process.env.REACT_APP_BACKEND_API_URL}task/distance`)
          
        }
        console.log("response: ", response.data)
        setRowData(response.data);
        setLoading(false); // Set loading to false when the response is received
      } catch (error) {
        console.error('There was an error!', error);
        setLoading(false); // Make sure to set loading to false in case of an error too
      }
    };

    return (
      <div className="center-horizontal center-vertical">
            <Navbar />
            {!authenticated && ( // Render the access code input if not authenticated
                <div className="access-code-container">
                    <h2>Please enter the 4-digit access code:</h2>
                    <input
                        type="password"
                        value={accessCode}
                        onChange={handleAccessCodeChange}
                    />
                    <button onClick={authenticate}>Submit</button>
                </div>
            )}
            {authenticated && ( // Render the main content if authenticated
                <div>
                    <div style={{ fontSize: 9, color: "#556B2F", fontFamily: 'Sans Serif', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                        <h1> Bid on RFP's Near You. </h1>
                    </div>
                    {/* Rest of your component content */}
                    <div className="home-banner-container" style={{ display: 'flex', alignItems: 'center' }}>
                        <Box sx={{ width: 700, marginRight: '25px' }}>
                            <Slider
                                aria-label="Miles"
                                defaultValue={10}
                                color="secondary"
                                marks={marks}
                                onChangeCommitted={(event, newValue) => {
                                    setSliderValue(newValue);
                                    handleCommit(event, newValue);
                                }}
                            />
                        </Box>
                        <DropdownMenu sliderValue={sliderValue} onValueChange={handleDropdownChange} /> {/* Render the dropdown menu here */}

                        {loading && ( // Render the spinner when loading is true
                            <div style={{ display: 'flex', justifyContent: 'center', marginTop: '50px' }}>
                                <Audio
                                    height={80}
                                    width={80}
                                    radius={9}
                                    color="green"
                                    ariaLabel="loading"
                                    wrapperStyle={{ display: 'flex', justifyContent: 'center' }}
                                />
                            </div>
                        )}
                        {!loading && rowData.length == 0 && (<Load></Load>)}
                        {!loading && rowData.length > 0 && (
                            <div style={{ height: 'auto', maxWidth: '1500px', margin: '0 auto', marginTop: '50px' }}>
                                <DataGrid
                                    rows={filterRowDataByBidType()}
                                    columns={columns}
                                    pageSize={5}
                                />
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};
  export default Home;
