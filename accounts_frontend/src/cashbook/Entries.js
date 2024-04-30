import React from 'react';

export default function Entries() {
    return (
        <div className='full-screen' style={{ backgroundImage: "url('https://thumbs.dreamstime.com/z/scrap-blue-paper-clips-gray-background-text-general-ledger-224920595.jpg')" }}>
            <form action="add" method="post">
                {/* CSRF token if needed */}
                {/* {% csrf_token %} */}
                {/* Display messages if any */}
                {/* {% for message in messages %} */}
                <h2 style={{ marginLeft: '600px', color: 'aqua' }}>{/* {message} */}</h2>
                {/* {% endfor %} */}
                <div className="form-outline mb-4" style={{ paddingLeft: '500px', margin: 'auto', width: '50%', paddingBottom: '20px', paddingTop: '10px' }}>
                    <input type="date" style={{ height: '30px', paddingRight: '24px' }} name="date" id="registerName" className="form-control" placeholder="Date" required />
                    <br />
                    <br />
                    <select id="types" name="types">
                        <option value="receipt">RECEIPT</option>
                        <option value="payment">PAYMENT</option>
                    </select>
                </div>
                <div className="form-outline mb-4" style={{ paddingLeft: '500px', margin: 'auto', width: '50%', paddingBottom: '20px' }}>
                    <input type="text" name="particulars" style={{ height: '30px' }} id="registerUsername" className="form-control" placeholder="Particulars" required />
                </div>
                <div className="form-outline mb-4" style={{ paddingLeft: '500px', margin: 'auto', width: '50%', paddingBottom: '20px' }}>
                    <input type="text" name="detail" style={{ height: '30px' }} id="registerEmail" className="form-control" placeholder="Detail" />
                </div>
                <div className="form-outline mb-4" style={{ paddingLeft: '500px', margin: 'auto', width: '50%', paddingBottom: '7px' }}>
                    <input type="number" name="amount" style={{ height: '30px' }} id="registerEmail" className="form-control" placeholder="Amount" required />
                </div>
                <br />
                <div style={{ paddingLeft: '600px', margin: 'auto', width: '50%', paddingBottom: '7px' }}>
                    <button type="submit" style={{ color: 'black', backgroundColor: 'lightgreen' }} className="btn btn-primary btn-block mb-3">ADD</button>
                </div>
            </form>
            <div style={{ paddingLeft: '550px', margin: 'auto', width: '50%', paddingBottom: '7px' }}>
                <button><a href="view" style={{ color: 'green', backgroundColor: 'transparent', textDecoration: 'none' }} className="btn btn-primary btn-block mb-3">View Cashbook</a></button>
            </div>
            <div style={{ paddingLeft: '550px', margin: 'auto', width: '50%', paddingBottom: '7px' }}>
                <button><a href="ledger" style={{ color: 'green', backgroundColor: 'transparent', textDecoration: 'none' }} className="btn btn-primary btn-block mb-3">View Ledger</a></button>
            </div>
        </div>
    );
}
