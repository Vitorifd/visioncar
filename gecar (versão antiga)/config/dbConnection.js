const mysql = require('mysql');

const connMysql = () => (
    mysql.createConnection({
        host: 'localhost',
        user: 'root',
        password: '',
        database: 'gecar'
    })
);

module.exports = () => connMysql;