create table doc (
doc_id uuid primary key,
subject text,
url text,
tags set<text>,
read_count int,
reply_count int,
charpter_count int,
created_at timestamp,
updated_at timestamp);

alter table doc add content text;