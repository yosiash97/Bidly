// Bid.js
import React from 'react';
import Button from '@mui/material/Button';

const Bid = ({ color, disabled, onClick }) => {
    console.log('Bid render', { onClick }); // Add this line to check if onClick is passed
    return (
        <Button disabled={disabled} onClick={() => {
            console.log('Button clicked'); // This will confirm the click is registered
            onClick(); // Make sure onClick is called
        }} style={{ color: 'white', backgroundColor: color }}>
            BID!
        </Button>
    );
};

export default Bid;
