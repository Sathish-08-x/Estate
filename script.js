function updateDashboard() {
    var stages = [];
    var leadsTable = document.querySelector('table:not(#followtable)');
    var dropdowns = leadsTable ? leadsTable.querySelectorAll('.stage') : [];
    
    if (dropdowns.length > 0) {
        dropdowns.forEach(function(selectBox) {
            stages.push(selectBox.value);
        });
        localStorage.setItem('leadStages', JSON.stringify(stages));
    } else {
        var saved = localStorage.getItem('leadStages');
        if (saved) {
            stages = JSON.parse(saved);
        } else {
            stages = ["new", "new", "new", "new", "new", "new", "new"];
        }
    }

    var activeCount = 0;
    var visitCount = 0;
    var negotiationCount = 0;
    var closedCount = 0;

    stages.forEach(function(stage) {
        var currentStage = stage.toLowerCase();
        if (currentStage === "new" || currentStage === "contacted" || currentStage === "qualified") {
            activeCount++;
        } else if (currentStage === "site-visit") {
            visitCount++;
        } else if (currentStage === "negotiation") {
            negotiationCount++;
        } else if (currentStage === "closed") {
            closedCount++;
        }
    });

    var v1 = document.getElementById('visit1');
    var v2 = document.getElementById('visit2');
    var v3 = document.getElementById('visit3');
    var v4 = document.getElementById('visit4');

    if (v1) v1.innerText = activeCount;
    if (v2) v2.innerText = visitCount;
    if (v3) v3.innerText = negotiationCount;
    if (v4) v4.innerText = closedCount;
}

function updatePipeline() {
    var board = document.querySelector('.pipboard');
    if (!board) return;

    var columns = board.querySelectorAll('.pipecl .clmncrds');
    if (columns.length < 4) return;

    var newCol = columns[0];
    var contactCol = columns[1];
    var negCol = columns[2];
    var closedCol = columns[3];

    newCol.innerHTML = '';
    contactCol.innerHTML = '';
    negCol.innerHTML = '';
    closedCol.innerHTML = '';

    var allLeads = [
        { name: "Ms.Amith Varma", type: "Buyer", interest: "Apartment", budget: "3 Cr", priority: "High" },
        { name: "Aditya", type: "Seller", interest: "House", budget: "1.25 Cr", priority: "Medium" },
        { name: "Mokshagan", type: "Buyer", interest: "Apartment", budget: "2 Cr", priority: "Low" },
        { name: "Sai Praveen", type: "Seller", interest: "Condo", budget: "3.5 Cr", priority: "High" },
        { name: "Datta Sai", type: "Buyer", interest: "Condo", budget: "2.7 Cr", priority: "High" },
        { name: "Shiva Sai", type: "Buyer", interest: "House", budget: "4 Cr", priority: "High" },
        { name: "Bala Sai", type: "Seller", interest: "House", budget: "3.5 Cr", priority: "High" }
    ];

    var customLeads = JSON.parse(localStorage.getItem('customLeads') || '[]');
    customLeads.forEach(function(cl) {
        allLeads.push({
            name: cl.name,
            type: cl.type,
            interest: cl.interest,
            budget: cl.budget,
            priority: cl.priority
        });
    });

    var savedStages = localStorage.getItem('leadStages');
    var stages = savedStages ? JSON.parse(savedStages) : null;

    allLeads.forEach(function(lead, index) {
        var stage = "new";
        if (stages && stages[index]) {
            stage = stages[index].toLowerCase();
        } else {
            if (index === 2) stage = "site-visit";
            else if (index === 3 || index === 4) stage = "negotiation";
            else stage = "new";
        }

        var pClass = "lead-low";
        var p = (lead.priority || "").toLowerCase();
        if (p.includes("high")) {
            pClass = "lead-high";
        } else if (p.includes("medium")) {
            pClass = "lead-medium";
        }

        var icon = "🏠 ";
        var intr = (lead.interest || "").toLowerCase();
        if (intr.includes("house")) {
            icon = "🏡 ";
        } else if (intr.includes("condo")) {
            icon = "🏢 ";
        }

        var cleanBudget = lead.budget.replace(/💰/g, '').trim();

        var card = document.createElement('div');
        card.className = pClass;
        card.innerHTML = '<h4>' + lead.name + '</h4>' +
            '<p class="crdbudg">💰 ' + cleanBudget + '</p>' +
            '<p class="crdtyp">' + icon + lead.interest + '</p>';

        if (stage === "site-visit" || stage === "contacted") {
            contactCol.appendChild(card);
        } else if (stage === "negotiation") {
            negCol.appendChild(card);
        } else if (stage === "closed") {
            closedCol.appendChild(card);
        } else {
            newCol.appendChild(card);
        }
    });

    if (newCol.children.length === 0) {
        newCol.innerHTML = '<div class="emptyeholder">No new leads</div>';
    }
    if (contactCol.children.length === 0) {
        contactCol.innerHTML = '<div class="emptyeholder">No contacted leads</div>';
    }
    if (negCol.children.length === 0) {
        negCol.innerHTML = '<div class="emptyeholder">No leads in negotiation</div>';
    }
    if (closedCol.children.length === 0) {
        closedCol.innerHTML = '<div class="emptyeholder">No deals closed yet</div>';
    }
}

function updateFollowup() {
    var followTable = document.getElementById('followtable');
    if (!followTable) return;

    var savedStages = localStorage.getItem('leadStages');
    var stages = savedStages ? JSON.parse(savedStages) : null;

    var rows = followTable.querySelectorAll('tr');
    var totalScheduled = 0;
    var highPriority = 0;
    var siteVisits = 0;
    var closedWon = 0;

    for (var i = 1; i < rows.length; i++) {
        var row = rows[i];
        totalScheduled++;

        var priority = row.cells[3] ? row.cells[3].innerText.toLowerCase() : "";
        if (priority.includes('high')) {
            highPriority++;
        }

        if (stages && stages[i - 1]) {
            var st = stages[i - 1].toLowerCase();
            var stageName = "New";
            var statusName = "Pending";
            if (st === "site-visit") {
                stageName = "Site Visisted Schedule";
                statusName = "Scheduled";
                siteVisits++;
            } else if (st === "negotiation") {
                stageName = "In negotiation";
                statusName = "Active";
            } else if (st === "closed") {
                stageName = "Closed Won";
                statusName = "Won";
                closedWon++;
            }
            if (row.cells[6]) row.cells[6].innerText = stageName;
            if (row.cells[7]) row.cells[7].innerText = statusName;
        } else {
            var currentStageText = row.cells[6] ? row.cells[6].innerText.toLowerCase() : "";
            if (currentStageText.includes('site')) siteVisits++;
            if (currentStageText.includes('closed')) closedWon++;
        }
    }

    var f1 = document.getElementById('follow1');
    var f2 = document.getElementById('follow2');
    var f3 = document.getElementById('follow3');
    var f4 = document.getElementById('follow4');

    if (f1) f1.innerText = totalScheduled;
    if (f2) f2.innerText = highPriority;
    if (f3) f3.innerText = siteVisits;
    if (f4) f4.innerText = closedWon;
}

function init() {
    var leadsTable = document.querySelector('table:not(#followtable)');
    if (leadsTable && !leadsTable.dataset.customLoaded) {
        leadsTable.dataset.customLoaded = "true";
        var customLeads = JSON.parse(localStorage.getItem('customLeads') || '[]');
        var tbody = leadsTable.querySelector('tbody') || leadsTable;
        customLeads.forEach(function(lead) {
            var row = document.createElement('tr');
            row.innerHTML = '<td>' + lead.name + '</td>' +
                '<td>' + lead.type + '</td>' +
                '<td>' + lead.interest + '</td>' +
                '<td>' + lead.budget + '</td>' +
                '<td>' + lead.stage + '</td>' +
                '<td>' + lead.priority + '</td>' +
                '<td>' + lead.date + '</td>' +
                '<td>' + lead.phone + '</td>' +
                '<td><select class="stage">' +
                    '<option value="new"' + (lead.stage.toLowerCase() === 'new' ? ' selected' : '') + '>New</option>' +
                    '<option value="site-visit"' + (lead.stage.toLowerCase() === 'site-visit' ? ' selected' : '') + '>Site Visisted Schedule</option>' +
                    '<option value="negotiation"' + (lead.stage.toLowerCase() === 'negotiation' ? ' selected' : '') + '>In negotiation</option>' +
                    '<option value="closed"' + (lead.stage.toLowerCase() === 'closed' ? ' selected' : '') + '>Closed Won</option>' +
                '</select>' +
                '<button type="button" class="savebtn">Save</button></td>';
            tbody.appendChild(row);
        });
    }

    if (leadsTable) {
        var savedStages = localStorage.getItem('leadStages');
        if (savedStages) {
            var stages = JSON.parse(savedStages);
            var dropdowns = leadsTable.querySelectorAll('.stage');
            dropdowns.forEach(function(selectBox, index) {
                if (stages[index]) {
                    selectBox.value = stages[index];
                    var row = selectBox.closest('tr');
                    if (row && row.cells.length > 4) {
                        row.cells[4].innerText = selectBox.options[selectBox.selectedIndex].text;
                    }
                }
            });
        }
    }

    var followTable = document.getElementById('followtable');
    if (followTable && !followTable.dataset.customLoaded) {
        followTable.dataset.customLoaded = "true";
        var customLeadsList = JSON.parse(localStorage.getItem('customLeads') || '[]');
        var ftbody = followTable.querySelector('tbody') || followTable;
        customLeadsList.forEach(function(lead) {
            var row = document.createElement('tr');
            var isClosed = lead.stage.toLowerCase() === 'closed';
            var isSite = lead.stage.toLowerCase() === 'site-visit';
            var stat = isClosed ? 'Won' : (isSite ? 'Scheduled' : 'Pending');
            row.innerHTML = '<td>' + lead.name + '</td>' +
                '<td>' + lead.type + '</td>' +
                '<td>' + lead.interest + '</td>' +
                '<td>' + lead.priority + '</td>' +
                '<td>' + lead.date + '</td>' +
                '<td>' + lead.phone + '</td>' +
                '<td>' + lead.stage + '</td>' +
                '<td>' + stat + '</td>';
            ftbody.appendChild(row);
        });
    }

    updateDashboard();
    updatePipeline();
    updateFollowup();
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

document.addEventListener('click', function(event) {
    if (event.target.classList.contains('savebtn')) {
        var tr = event.target.closest('tr');
        if (tr) {
            var sel = tr.querySelector('.stage');
            if (sel && tr.cells.length > 4) {
                tr.cells[4].innerText = sel.options[sel.selectedIndex].text;
            }
        }

        var leadsTable = document.querySelector('table:not(#followtable)');
        if (leadsTable) {
            var dropdowns = leadsTable.querySelectorAll('.stage');
            var stages = [];
            var customLeads = JSON.parse(localStorage.getItem('customLeads') || '[]');

            dropdowns.forEach(function(selectBox, idx) {
                stages.push(selectBox.value);
                var row = selectBox.closest('tr');
                if (row && row.cells.length > 4) {
                    row.cells[4].innerText = selectBox.options[selectBox.selectedIndex].text;
                }
                if (idx >= 7 && customLeads[idx - 7]) {
                    customLeads[idx - 7].stage = selectBox.options[selectBox.selectedIndex].text;
                }
            });

            localStorage.setItem('leadStages', JSON.stringify(stages));
            localStorage.setItem('customLeads', JSON.stringify(customLeads));
        }

        updateDashboard();
        updatePipeline();
        updateFollowup();
        alert("Stage updated successfully!");
    }

    if (event.target.matches('input[type="submit"]') || event.target.value === 'Sumbit leed') {
        event.preventDefault();

        var nameInput = document.querySelector('input[name="client-Name"]');
        var clientName = nameInput ? nameInput.value.trim() : "";

        if (!clientName) {
            alert("Please enter client name!");
            return;
        }

        var sellerRadio = document.querySelector('input[value="seller"]');
        var clientType = (sellerRadio && sellerRadio.checked) ? "Seller" : "Buyer";

        var selects = document.querySelectorAll('.content select');
        var interest = selects[0] ? selects[0].value : "Apartment";
        var leadStage = selects[1] ? selects[1].value : "New";
        var priority = selects[2] ? selects[2].value : "High";

        var budgetInput = document.querySelector('input[name="budget"]');
        var budgetVal = budgetInput ? budgetInput.value.trim() : "";
        var budget = budgetVal ? (budgetVal.includes('cr') ? budgetVal : budgetVal + 'cr') : "";

        var dateInput = document.querySelector('input[name="follow-up-date"]');
        var followUpDate = dateInput ? dateInput.value : "";

        var customLeads = JSON.parse(localStorage.getItem('customLeads') || '[]');
        customLeads.push({
            name: clientName,
            type: clientType,
            interest: interest,
            budget: budget,
            stage: leadStage,
            priority: priority,
            date: followUpDate,
            phone: "*******" + Math.floor(100 + Math.random() * 900)
        });
        localStorage.setItem('customLeads', JSON.stringify(customLeads));

        var savedStages = localStorage.getItem('leadStages');
        var stages = savedStages ? JSON.parse(savedStages) : ["new", "new", "new", "new", "new", "new", "new"];
        stages.push(leadStage.toLowerCase());
        localStorage.setItem('leadStages', JSON.stringify(stages));

        updateDashboard();
        updatePipeline();
        updateFollowup();

        nameInput.value = "";
        if (budgetInput) budgetInput.value = "";
        if (dateInput) dateInput.value = "";
        var buyerRadio = document.querySelector('input[value="buyer"]');
        if (buyerRadio) buyerRadio.checked = true;
        if (sellerRadio) sellerRadio.checked = false;

        alert("Lead submitted successfully!");
    }
});