import React, { useState, useEffect } from "react";
import '../DropdownMenu.css'; // Make sure to create this CSS file
import axios from "axios";


const DropdownMenu = ({sliderValue, onValueChange}) => {
    const [selectedValue, setSelectedValue] = useState('');

    const handleDropdownChange = (event) => {
        const newValue = event.target.value;
        setSelectedValue(newValue); // Update internal state
        onValueChange(newValue); // Propagate change to parent component
    };

    return (
        <div>
            <select value={selectedValue} onChange={handleDropdownChange}>
                <option value="">Return All Bid Types</option>
                <option value="civil_engineering">Civil Engineering</option>
                <option value="construction">Construction</option>
            </select>
        </div>
    );
};

export default DropdownMenu;