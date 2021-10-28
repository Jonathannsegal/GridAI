// Authors: Abhilash Tripathy
// Created: 1/25/2021
// Updated: 5/3/2021
// Copyrighted 2021 sdmay21-23@iastate.edu
import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';

const useStyles = makeStyles({
  table: {
    minWidth: 650,
  },
});

const DenseTableHead = (props) => {
  const tableDataRow_0 = props.firstRow;
  const rowProperties = [];
  for(const property in tableDataRow_0) {
    rowProperties.push(property);
  }

  return (
    <TableHead>
      <TableRow>
        {rowProperties.map((property) => (
          <TableCell align="center"><b>{property}&nbsp;</b></TableCell>
        ))}
      </TableRow>
    </TableHead>
  );
}

const DenseTableRow = (props) => {
  const tableDataRow = props.row;
  const rowProperties = [];
  for(const property in tableDataRow) {
    rowProperties.push(tableDataRow[property]);
  }

  return (
    <TableRow>
      {rowProperties.map((propertyValue) => (
        <TableCell align="center">{propertyValue}&nbsp;</TableCell>
      ))}
    </TableRow>
  );
}

const DenseTable = (props) => {
  const classes = useStyles();

  const tableData = props.data;
  const columnNames = props.columnNames;

  console.log('tableData=', tableData);
  return (
    <TableContainer component={Paper}>
      {
        (!tableData)||(tableData.length==0)
        ? <div></div>
        :
        <Table className={classes.table} size="small" aria-label="a dense table">
            {/* <TableHead>
              
              <TableRow>
                {columnNames.map((col) => (
                  <TableCell align="left">{col}&nbsp;</TableCell>
                ))}

              </TableRow>

            </TableHead> */}
            <DenseTableHead firstRow={tableData[0]} />
            <TableBody>

              {tableData.map((row) => (
                <DenseTableRow row={row} />
              ))}
              
            </TableBody>
          </Table>
      }
    </TableContainer>
  );
}

export default DenseTable;
