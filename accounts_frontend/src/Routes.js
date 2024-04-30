import React from "react";

import {
    BrowserRouter as Router,
    Routes,
    Route
  } from "react-router-dom";
import Entries from "./cashbook/Entries";
import ViewEntries from "./cashbook/ViewEntries";


export default function Routers() {
    return (
        <Router>
            <Routes>
                <Route path='/add' exact element={<Entries />}></Route>
                <Route path='/view' exact element={<ViewEntries />}></Route>
            </Routes>
        </Router>
    )
}