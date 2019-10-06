class OfficialsDAO {

    constructor(connection) {
        this.connection = connection();
    }

    getOne(carPlate, callback) {
        this.connection.query(`SELECT * FROM official WHERE car_plate_official = '${carPlate}'`, callback);
    }
}

module.exports = () => OfficialsDAO;