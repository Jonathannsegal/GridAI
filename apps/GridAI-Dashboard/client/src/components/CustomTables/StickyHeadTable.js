// Authors: Abhilash Tripathy
// Created: 1/25/2021
// Updated: 5/3/2021
// Copyrighted 2021 sdmay21-23@iastate.edu
import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TablePagination from '@material-ui/core/TablePagination';
import TableRow from '@material-ui/core/TableRow';

const StickyHeadTableHead = (props) => {
    const tableDataRow_0 = props.firstRow;
    const rowProperties = [];
    for(const property in tableDataRow_0) {
      rowProperties.push(property);
    }
  
    return (
      <TableHead>
        <TableRow>
          {rowProperties.map((property) => (
            <TableCell align="left"><b>{property}&nbsp;</b></TableCell>
          ))}
        </TableRow>
      </TableHead>
    );
  }
  
const StickyHeadTableRow = (props) => {
    const tableDataRow = props.row;
    const tableDataRowIndex = props.rowNum;
    const rowProperties = [];
    for(const property in tableDataRow) {
      rowProperties.push(tableDataRow[property]);
    }
  
    return (
      <TableRow hover role="checkbox" tabIndex={-1}>
        {rowProperties.map((propertyValue, cellIndex) => (
            <TableCell align="left" key={"row"+tableDataRowIndex+"cell"+cellIndex}>
                {propertyValue}&nbsp;
            </TableCell>
        ))}
      </TableRow>
    );
  }

const useStyles = makeStyles({
  root: {
    width: '100%',
  },
  container: {
    maxHeight: 440,
  },
});

const StickyHeadTable = (props) => {
    const classes = useStyles();
    const [page, setPage] = React.useState(0);
    const [rowsPerPage, setRowsPerPage] = React.useState(10);

    let tableData = props.data;
    const {filterBy, propToFilter} = props;

    if(filterBy && filterBy!=' ALL') {
      tableData = tableData.filter(item => item[propToFilter] == filterBy);
    }

    const handleChangePage = (event, newPage) => {
      setPage(newPage);
    };

    const handleChangeRowsPerPage = (event) => {
      setRowsPerPage(+event.target.value);
      setPage(0);
    };

    return (
    <Paper className={classes.root}>
        <TableContainer className={classes.container}>
        <Table stickyHeader aria-label="sticky table">
            <StickyHeadTableHead firstRow={tableData[0]} />
            <TableBody>
                {tableData
                .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                .map((row, rowIndex) => <StickyHeadTableRow row={row} rowNum={rowIndex} />)}
            </TableBody>
        </Table>
        </TableContainer>
        <TablePagination
        rowsPerPageOptions={[10, 25, 100]}
        component="div"
        count={tableData.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onChangePage={handleChangePage}
        onChangeRowsPerPage={handleChangeRowsPerPage}
        />
    </Paper>
  );
}

export default StickyHeadTable;
