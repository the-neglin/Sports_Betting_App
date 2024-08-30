def load_notice():
    load_picks_notice = """
                $(document).ready(function() {
                    console.log("Inline JavaScript loaded");
                    $('#load_picks').click(function() {
                        var modalId = 'loadPicksModal';  // Unique ID for this modal
                        var modalHtml = '<div class="modal fade" id="' + modalId + '" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">' +
                                        '<div class="modal-dialog modal-dialog-centered">' +  // Center the modal
                                        '<div class="modal-content">' +
                                        '<div class="modal-header">' +
                                        '<h5 class="modal-title" id="exampleModalLabel">Notification</h5>' +
                                        '<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>' +
                                        '</div>' +
                                        '<div class="modal-body">' +
                                        'Your picks have been loaded.' +
                                        '</div>' +
                                        '<div class="modal-footer">' +
                                        '<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>' +
                                        '</div>' +
                                        '</div>' +
                                        '</div>' +
                                        '</div>';
                        $('body').append(modalHtml);
                        var myModal = new bootstrap.Modal(document.getElementById(modalId), {});
                        myModal.show();
                    });
                });
            """
    return load_picks_notice

def submit_notice():
    submit_picks_notice = """
                $(document).ready(function() {
                    console.log("Inline JavaScript loaded");
                    $('#submit_picks').click(function() {
                        var modalId = 'submitPicksModal';  // Unique ID for this modal
                        var modalHtml = '<div class="modal fade" id="' + modalId + '" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">' +
                                        '<div class="modal-dialog modal-dialog-centered">' +  // Center the modal
                                        '<div class="modal-content">' +
                                        '<div class="modal-header">' +
                                        '<h5 class="modal-title" id="exampleModalLabel">Notification</h5>' +
                                        '<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>' +
                                        '</div>' +
                                        '<div class="modal-body">' +
                                        'Your picks have been submitted.' +
                                        '</div>' +
                                        '<div class="modal-footer">' +
                                        '<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>' +
                                        '</div>' +
                                        '</div>' +
                                        '</div>' +
                                        '</div>';
                        $('body').append(modalHtml);
                        var myModal = new bootstrap.Modal(document.getElementById(modalId), {});
                        myModal.show();
                    });
                });
            """
    return submit_picks_notice


def form_completion():
    form_complete = """
        // JavaScript to enable/disable the button based on input fields
        document.addEventListener('DOMContentLoaded', function() {
            const nameInput = document.getElementById('name');
            const emailInput = document.getElementById('email');
            const loadPicksButton = document.getElementById('load_picks');

            function checkFormCompletion() {
                if (nameInput.value.trim() && emailInput.value.trim()) {
                    loadPicksButton.disabled = false;
                } else {
                    loadPicksButton.disabled = true;
                }
            }

            // Check form completion on input change
            nameInput.addEventListener('input', checkFormCompletion);
            emailInput.addEventListener('input', checkFormCompletion);
        });
    """
    return form_complete

def double_check():
    double_down = """
        function enforceSingleCheckboxSelection() {
            console.log("Enforcing single checkbox selection...");  // Debug log
            const checkboxes = document.querySelectorAll('input[type="checkbox"][id^="double_down_"]');

            checkboxes.forEach(checkbox => {
                checkbox.addEventListener('change', function() {
                    console.log("Checkbox state changed: ", this.id);  // Debug log
                    if (this.checked) {
                        checkboxes.forEach(otherCheckbox => {
                            if (otherCheckbox !== this) {
                                otherCheckbox.checked = false;
                            }
                        });
                    }
                });
            });
        }

        document.addEventListener('DOMContentLoaded', () => {
            console.log("DOM fully loaded and parsed");  // Debug log
            enforceSingleCheckboxSelection();
        });

        Shiny.addCustomMessageHandler('reapply_checkbox_script', function() {
            console.log("Reapplying checkbox script...");  // Debug log
            enforceSingleCheckboxSelection();
        });
    """
    return double_down

def too_late():
    too_late =     """
    document.addEventListener('DOMContentLoaded', function() {
        const rows = document.querySelectorAll('table tr');

        function parseDateTime(datetimeText) {
            // Example: "Thursday, 09/05 07:20 PM CT"
            const [dayOfWeek, monthDay, time, period, timezone] = datetimeText.split(/[, ]+/);

            const [month, day] = monthDay.split('/');
            const [hours, minutes] = time.split(':');
            const isPM = period === 'PM';

            // Convert to 24-hour format
            let hours24 = parseInt(hours, 10);
            if (isPM && hours24 < 12) hours24 += 12;
            if (!isPM && hours24 === 12) hours24 = 0;

            // Construct date string in ISO format
            const now = new Date();
            const year = now.getFullYear();
            const isoDateString = `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}T${hours24.toString().padStart(2, '0')}:${minutes.padStart(2, '0')}:00`;

            return new Date(isoDateString);
        }

        const currentDateTime = new Date();

        rows.forEach(row => {
            const timeCell = row.cells[0]; // Assuming the datetime is in the first column
            const datetimeText = timeCell.textContent.trim();
            const rowDateTime = parseDateTime(datetimeText);

            if (currentDateTime.getTime() > rowDateTime.getTime()) {
                const inputs = row.querySelectorAll('input, select, textarea');
                inputs.forEach(input => {
                    input.disabled = true;
                });
            }
        });
    });
    """
    return too_late