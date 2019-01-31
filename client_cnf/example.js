var Client = require('mariadb');

var c = new Client(read_default_file="~/.my.cnf");

c.query('SELECT @@version as ver;', function(err, rows) {
    console.dir(rows[0]['ver']);
});
c.end();

