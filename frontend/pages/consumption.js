/* eslint-disable linebreak-style */
/* eslint-disable no-unused-vars */
/* eslint-disable import/no-extraneous-dependencies */
/* eslint-disable import/extensions */
/* eslint-disable react/prop-types */
import * as React from 'react';
import Metatags from '../components/Metatags';
import HexagonMap from '../components/ConsumptionHexagonMap';

export default function Hexagon() {
  return (
    <main>
      <Metatags title="Grid AI" description="GridAI" />

      <section className="w-full h-96 bg-white">

        <div className="mx-auto max-w-7xl">
          <div className="flex flex-col lg:flex-row">
            <div className="relative w-full bg-cover">
              <div className="relative flex flex-col items-center justify-center w-full h-full px-0 my-0 lg:px-10 lg:my-0">
                <div className="container px-8 mx-auto h-96 sm:px-0 xl:px-0">
                  <div id="Map" className="w-full px-0 py-0 mx-auto mt-5 bg-white border border-gray-200 rounded-lg sm:px-0 md:px-0 sm:py-0 sm:shadow">
                    <HexagonMap />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

      </section>

    </main>
  );
}
