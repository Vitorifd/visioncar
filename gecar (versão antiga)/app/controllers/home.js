module.exports.index = (app, req, res) => {

    const connection = app.config.dbConnection;

    const ReportsDAO = new app.app.models.ReportsDAO(connection);

    ReportsDAO.getAll((error, result) => {

        res.render('reports', { reports: result });
    });
}

module.exports.addReport = (app, req, res) => {

    const carPlate = req.body.carPlate;
    const connection = app.config.dbConnection;

    const ReportsDAO = new app.app.models.ReportsDAO(connection);
    const OfficialsDAO = new app.app.models.OfficialsDAO(connection);

    OfficialsDAO.getOne(carPlate, (error, result) => {

        if (result.length === 1) {
            const official = result[0];

            const date = new Date();
            const day = date.getDate();
            const month = date.getMonth() + 1;
            const year = date.getFullYear();
            const hours = date.getHours();
            const minutes = date.getMinutes();
            const seconds = date.getSeconds();

            const compareDate = `${year}-${month}-${day} ${hours}:${minutes - 1}:${seconds}`;
            const formatedDate = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;

            ReportsDAO.getOne(official.id_official, compareDate, (err, resul) => {

                if(resul.length === 0)
                    ReportsDAO.insertNew(formatedDate, official.id_official);

            });
        }
    });

    res.send();
}