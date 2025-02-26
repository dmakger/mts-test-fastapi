$(document).ready(function() {
    // Инициализация Tabs
    $("#tabs").tabs({
        active: 0
    });

    // Инициализация DatePicker
    $("#reportDate").datepicker({
        dateFormat: "yy-mm-dd",
        maxDate: 0
    });

    // Инициализация Select2
    $("#divisions").select2();

    // Запрос на получение данных сотрудников
    async function fetchEmployeesData(reportDate = null, divisions = []) {
        try {
            const url = new URL("http://localhost:8000/api/v1/employees/all");
            const params = new URLSearchParams();

            if (reportDate) {
                params.append("reportDate", reportDate);
            }

            if (divisions.length > 0) {
                params.append("divisions", JSON.stringify(divisions));
            }

            url.search = params.toString();

            const response = await fetch(url, {
                method: "GET", // Тип запроса
                headers: {
                    "Content-Type": "application/json",
                },
            });

            // Проверяем, успешен ли запрос
            if (!response.ok) {
                throw new Error(`Error fetching employees: ${response.statusText}`);
            }

            // Извлекаем данные из ответа
            const employeesData = await response.json();
            return employeesData; // Возвращаем данные для дальнейшего использования

        } catch (error) {
            console.error("Error in fetchEmployeesData:", error);
            throw error; // Перехватываем и пробрасываем ошибку
        }
    }

    // Получение данных сотрудников при загрузке страницы
    async function loadEmployees() {
        try {
            // Получаем данные сотрудников без фильтров по умолчанию
            const employeesData = await fetchEmployeesData();

            // Заполняем таблицу сотрудников
            const employeesTable = $('#employeesTable').DataTable({
                data: employeesData,
                columns: [
                    { data: 'fio' },
                    { data: 'position' },
                    { data: 'division' },
                    { data: 'head' },
                    { data: 'hire_date' },
                    { data: 'dismissal_date' },
                    { data: 'employment_type' },
                    { data: 'salary' }
                ]
            });

            // Заполняем Select2
            const divisionsData = Array.from(new Set(employeesData.map(emp => emp.division))); // Извлекаем уникальные подразделения
            divisionsData.forEach(division => {
                $("#divisions").append(new Option(division, division));
            });

        } catch (error) {
            console.error("Error loading employees:", error);
        }
    }

    // Инициализация данных сотрудников при загрузке страницы
    loadEmployees();

    // Обновление таблицы сотрудников при изменении даты
    $("#reportDate").on("change", async function() {
        const selectedDate = $(this).val();
        const selectedDivisions = $("#divisions").val() || [];

        // Получаем обновленные данные с учетом выбранной даты и подразделений
        const employeesData = await fetchEmployeesData(selectedDate, selectedDivisions);

        // Перезагружаем таблицу с новыми данными
        const employeesTable = $('#employeesTable').DataTable();
        employeesTable.clear().rows.add(employeesData).draw();
    });

    // Обновление таблицы подразделений при изменении выбора
    $("#divisions").on("change", async function() {
        const selectedDivisions = $(this).val() || [];
        const selectedDate = $("#reportDate").val();

        // Получаем обновленные данные с учетом выбранных подразделений и даты
        const employeesData = await fetchEmployeesData(selectedDate, selectedDivisions);

        // Перезагружаем таблицу с новыми данными
        const employeesTable = $('#employeesTable').DataTable();
        employeesTable.clear().rows.add(employeesData).draw();
    });
});
