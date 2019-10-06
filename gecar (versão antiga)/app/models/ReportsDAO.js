class ReportsDAO{

    constructor(connection){
        this.connection = connection();
    }

    getAll(callback) {
        this.connection.query("SELECT name_official, DATE_FORMAT(schedule_report, '%m/%d/%Y %H:%i') as schedule_report FROM report, official WHERE id_official = id_official_report", callback);
    }

    getOne(idOfficial, date, callback) {
        this.connection.query(`SELECT * FROM report WHERE id_official_report = '${idOfficial}' AND schedule_report > '${date}'`, callback);
    }

    insertNew(scheduleReport, idOfficial){
        this.connection.query(`INSERT INTO report(schedule_report, id_official_report) VALUES('${scheduleReport}', ${idOfficial})`);
    }
}

module.exports = () => ReportsDAO;