import React from 'react';

const TableRow = ({ data }) => {
  return (
    <tr>
      <td>{data.id}</td>
      <td>{data.name}</td>
    </tr>
  );
};

export default TableRow;
