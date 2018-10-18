drop table if exists entries;
create table SongVideos (
  id integer primary key autoincrement,
  title text not null,
  comments text not null,
);