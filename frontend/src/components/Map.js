import React, { useEffect } from 'react';
import * as atlas from 'azure-maps-control';

const Maps = () => {
    useEffect(() => {
        const map = new atlas.Map('myMap', {
            center: [-122.33, 47.6],
            zoom: 12,
            view: 'Auto',
            authOptions: {
                authType: 'subscriptionKey',
                subscriptionKey: process.env.REACT_APP_AZURE_MAPS_KEY
            }
        });

        map.events.add('ready', function () {
            var marker = new atlas.HtmlMarker({
                color: 'DodgerBlue',
                text: 'M',
                position: [-122.33, 47.6]
            });
            map.markers.add(marker);
        });
    }, []);

    return (
        <div id='myMap' style={{ width: '100%', height: '600px' }}></div>
    );
};

export default Maps;
