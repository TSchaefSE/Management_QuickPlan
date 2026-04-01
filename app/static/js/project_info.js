
function addMemberRow() {
    const container = document.getElementById("team-members-list");

    const row = document.createElement("div");
    row.className = "member-row";

    row.innerHTML = `
        <input type="text" name="member_name[]" placeholder="Name">
        <input type="text" name="member_role[]" placeholder="Role">
        <input type="email" name="member_email[]" placeholder="Email">
        <button type="button" class="remove-btn" onclick="removeRow(this)">Remove</button>
    `;

    container.appendChild(row);
}

function addRiskRow() {
    const container = document.getElementById("risks-list");

    const row = document.createElement("div");
    row.className = "risk-row";

    row.innerHTML = `
        <input type="text" name="risk_name[]" placeholder="Risk Name">

        <select name="risk_priority[]">
            <option value="Low">Low</option>
            <option value="Medium">Medium</option>
            <option value="High">High</option>
        </select>

        <select name="risk_status[]">
            <option value="Open">Open</option>
            <option value="Mitigated">Mitigated</option>
            <option value="Closed">Closed</option>
        </select>

        <button type="button" class="remove-btn" onclick="removeRow(this)">Remove</button>
    `;

    container.appendChild(row);
}

function removeRow(button) {
    const row = button.parentElement;
    row.remove();
}