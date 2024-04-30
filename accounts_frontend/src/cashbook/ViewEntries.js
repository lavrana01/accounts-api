import React, { useEffect, useState } from 'react';
import GetEntries from './helper/corepapicalls';

export default function EntriesComponent() {
    const [entries, setEntries] = useState([]);

    useEffect(() => {
        const fetchData = () => {
            GetEntries()
                .then(data => {
                    if (data.Success) {
                        setEntries(data.Data);
                    } else {
                        console.error('Error fetching entries:', data.Message);
                    }
                })
                .catch(error => {
                    console.error('Error fetching entries:', error);
                });
        };

        fetchData();
    }, []);

    return (
        <div style={{ backgroundImage: `url('https://images.unsplash.com/photo-1553095066-5014bc7b7f2d?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8d2FsbCUyMGJhY2tncm91bmR8ZW58MHx8MHx8&w=1000&q=80')`, backgroundSize: 'cover', minHeight: '100vh', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
            <h1 style={{ color: 'white', marginBottom: '20px' }}>Cashbook Entries</h1>
            <table style={{ backgroundColor: '#009879', color: '#ffffff', borderCollapse: 'collapse', fontSize: '0.9em', fontFamily: 'sans-serif', width: '80%', boxShadow: '0 0 20px rgba(0,0,0,0.15)' }}>
                <thead>
                    <tr>
                        <th style={{ padding: '10px' }}>Date</th>
                        <th style={{ padding: '10px' }}>Type</th>
                        <th style={{ padding: '10px' }}>Particulars</th>
                        <th style={{ padding: '10px' }}>Detail</th>
                        <th style={{ padding: '10px' }}>Amount</th>
                        <th style={{ padding: '10px' }}>Cash In Hand</th>
                    </tr>
                </thead>
                <tbody>
                    {entries.map((entry, index) => (
                        <tr key={index} style={{ backgroundColor: 'white', color: 'black' }}>
                            <td style={{ padding: '10px' }}>{entry.date}</td>
                            <td style={{ padding: '10px' }}>{entry.type_of_entry}</td>
                            <td style={{ padding: '10px' }}>{entry.particulars}</td>
                            <td style={{ padding: '10px' }}>{entry.detail}</td>
                            <td style={{ padding: '10px' }}>{entry.amount}</td>
                            <td style={{ padding: '10px' }}>{entry.cash}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
