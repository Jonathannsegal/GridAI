import React, { useState } from 'react';
import { useFetch } from '../Endpoints/useFetch';
import Button from '@material-ui/core/Button';
import DenseTable from './DenseTable';
import StickyHeadTable from './StickyHeadTable';

// Testing purpose: dummy multi-property object array
const rows = [
    {CountryName:'India', ShortForm: 'IN', num1: 1324171354, num2: 3287263},
    {CountryName:'China', ShortForm: 'CN', num1: 1403500365, num2: 9596961},
    {CountryName:'Italy', ShortForm: 'IT', num1: 60483973, num2: 301340},
    {CountryName:'United States', ShortForm: 'US', num1: 327167434, num2: 9833520},
    {CountryName:'Canada', ShortForm: 'CA', num1: 37602103, num2: 9984670},
    {CountryName:'Australia', ShortForm: 'AU', num1: 25475400, num2: 7692024},
    {CountryName:'Germany', ShortForm: 'DE', num1: 83019200, num2: 357578},
    {CountryName:'Ireland', ShortForm: 'IE', num1: 4857000, num2: 70273},
    {CountryName:'Mexico', ShortForm: 'MX', num1: 126577691, num2: 1972550},
    {CountryName:'Japan', ShortForm: 'JP', num1: 126317000, num2: 377973},
    {CountryName:'France', ShortForm: 'FR', num1: 67022000, num2: 640679},
    {CountryName:'United Kingdom', ShortForm: 'GB', num1: 67545757, num2: 242495},
    {CountryName:'Russia', ShortForm: 'RU', num1: 146793744, num2: 17098246},
    {CountryName:'Nigeria', ShortForm: 'NG', num1: 200962417, num2: 923768},
    {CountryName:'Brazil', ShortForm: 'BR', num1: 210147125, num2: 8515767},
  ];

const TableAndButton = () => {
    // Replace useState(rows) with useState([])
    const [BusData, setBusData] = useState(rows);
    const show25 = useFetch('/show25', {});

    const show25data = () => {
        setBusData(show25.response);
        console.log(show25.response);
    }


    return (
        <div className="App" >
            {/* <DenseTable data={BusData} /> */}
            <StickyHeadTable data={BusData} />
            <Button onClick={show25data}>Reload</Button>
        </div>
    );
}

export default TableAndButton;