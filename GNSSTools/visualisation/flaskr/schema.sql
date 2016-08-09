# Tampere University of Technology
#
# DESCRIPTION
# Calls the html script. Processing functions are added.
# This file is launched on the browser
#
# AUTHOR
# Yannick DEFRANCE

drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  'text' text not null
);

sqlite3 /tmp/flaskr.db < schema.sql