import { API } from "../../backend";

export default function GetEntries() {
    return fetch(`${API}/view-cashbook-entries/`, {method: 'GET'})
    .then(response => {
        return response.json()
    })
    .catch(error => {
        console.log(error)
    })
}