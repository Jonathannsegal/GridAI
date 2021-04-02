import React from 'react';
import { Chart } from "react-google-charts";

const LineChart = (props) => {

    return(

        <Chart
          width={'600px'}
          height={'400px'}
          chartType="LineChart"
          loader={<div>Loading Chart</div>}
          data={props.data}
          options={{
            hAxis: {
              title: 'Transformer',
            },
            vAxis: {
              title: 'kWh',
            },
          }}
          rootProps={{ 'data-testid': '1' }}
        />
    )
}

export default LineChart;
