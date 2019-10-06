module.exports = app => {

    app.get('/', (req, res) => {
        app.app.controllers.home.index(app, req, res);
    });

    app.post('/', (req, res) => {
        app.app.controllers.home.addReport(app, req, res);
    });
}