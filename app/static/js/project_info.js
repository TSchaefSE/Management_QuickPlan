

function addMemberRow() {
    const container = document.getElementById("team-members-list");

    const row = document.createElement("tr");
    row.innerHTML = `
        <td><input type="text" name="member_name[]" placeholder="Name"></td>
        <td><input type="text" name="member_role[]" placeholder="Role"></td>
        <td><input type="email" name="member_email[]" placeholder="Email"></td>
        <td><button type="button" class="remove-link" onclick="removeRow(this)">Remove</button></td>
    `;

    container.appendChild(row);
}

function addRiskRow() {
    const container = document.getElementById("risks-list");

    const row = document.createElement("tr");
    row.innerHTML = `
        <td><input type="text" name="risk_name[]" placeholder="Risk Name"></td>

        <td>
            <select name="risk_priority[]">
                <option value="Low">Low</option>
                <option value="Medium">Medium</option>
                <option value="High">High</option>
            </select>
        </td>

        <td>
            <select name="risk_status[]">
                <option value="Open">Open</option>
                <option value="Mitigated">Mitigated</option>
                <option value="Closed">Closed</option>
            </select>
        </td>

        <td>
            <button type="button" class="remove-link" onclick="removeRow(this)">Remove</button>
        </td>
    `;

    container.appendChild(row);
}

function removeRow(button) {
    const row = button.closest("tr");
    if (row) {
        row.remove();
    }
}