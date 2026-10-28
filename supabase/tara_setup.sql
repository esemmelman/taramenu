create table public.taramenu_homework_documents (
 document_key text primary key check(document_key='homework'),
 content_html text not null default '', updated_at timestamptz not null default now()
);
alter table public.taramenu_homework_documents enable row level security;
grant select,update on public.taramenu_homework_documents to anon,authenticated;
create policy tara_homework_read on public.taramenu_homework_documents for select to anon,authenticated using(document_key='homework');
create policy tara_homework_update on public.taramenu_homework_documents for update to anon,authenticated using(document_key='homework') with check(document_key='homework');
insert into public.taramenu_homework_documents(document_key) values('homework');

create table public.taramenu_service_recordings_v1 (
 id uuid primary key, name text not null default 'Tara' check(name='Tara'),
 start_time timestamptz not null, passage_key_text text not null check(length(passage_key_text) between 1 and 120),
 mime_type text not null check(mime_type in ('audio/webm','audio/ogg','audio/mp4')),
 audio_base64 text not null check(length(audio_base64) between 1 and 12000000)
);
alter table public.taramenu_service_recordings_v1 enable row level security;
grant select,insert,update,delete on public.taramenu_service_recordings_v1 to anon;
create policy tara_current_service_recording on public.taramenu_service_recordings_v1 for all to anon
 using(id::text=(current_setting('request.headers',true)::jsonb->>'x-recording-id'))
 with check(id::text=(current_setting('request.headers',true)::jsonb->>'x-recording-id'));

create table public.tara_torah_passage_recordings_v1 (
 id uuid primary key, name text not null default 'Tara' check(name='Tara'),
 start_time timestamptz not null, passage_key text not null default 'exodus-8-1-15' check(passage_key='exodus-8-1-15'),
 mime_type text not null check(mime_type in ('audio/webm','audio/ogg','audio/mp4')),
 audio_base64 text not null check(length(audio_base64) between 1 and 12000000),
 start_time_pacific timestamp generated always as (start_time at time zone 'America/Los_Angeles') stored,
 playback_url text generated always as ('https://esemmelman.github.io/taramenu/torah/recording.html#' || id::text) stored
);
alter table public.tara_torah_passage_recordings_v1 enable row level security;
grant select,insert,update,delete on public.tara_torah_passage_recordings_v1 to anon;
create policy tara_current_torah_recording on public.tara_torah_passage_recordings_v1 for all to anon
 using(id::text=(current_setting('request.headers',true)::jsonb->>'x-recording-id'))
 with check(id::text=(current_setting('request.headers',true)::jsonb->>'x-recording-id'));

create table public.tara_torah_highlight_groups_v1 (
 id bigint generated always as identity primary key,
 passage_key text not null default 'exodus-8-1-15' check(passage_key='exodus-8-1-15'),
 verse smallint not null check(verse between 1 and 15),
 start_word smallint not null check(start_word>=0), end_word smallint not null check(end_word>=start_word),
 color smallint not null check(color in (1,2)), created_at timestamptz not null default now(),
 unique(passage_key,verse,start_word,end_word)
);
alter table public.tara_torah_highlight_groups_v1 enable row level security;
grant select on public.tara_torah_highlight_groups_v1 to anon;
create policy tara_group_read on public.tara_torah_highlight_groups_v1 for select to anon using(true);
create table public.tara_torah_group_recordings_v1 (
 highlight_group_id bigint primary key references public.tara_torah_highlight_groups_v1(id) on delete cascade,
 object_path text not null unique check(object_path like 'groups/%'),
 mime_type text not null check(mime_type in ('audio/webm','audio/ogg','audio/mp4')),
 byte_size bigint not null check(byte_size between 1 and 52428800), updated_at timestamptz not null default now()
);
alter table public.tara_torah_group_recordings_v1 enable row level security;
grant select on public.tara_torah_group_recordings_v1 to anon;
create policy tara_group_audio_read on public.tara_torah_group_recordings_v1 for select to anon using(true);
insert into storage.buckets(id,name,public,file_size_limit,allowed_mime_types)
 values('tara-torah-group-recordings-v1','tara-torah-group-recordings-v1',true,52428800,array['audio/webm','audio/ogg','audio/mp4']);

create table public.tara_mitzvah_status_items_v1 (
 item_key text primary key, label text not null, sort_order integer not null unique
);
create table public.tara_mitzvah_status_dates_v1 (
 date_key text primary key, label text not null, sort_order integer not null unique
);
create table public.tara_mitzvah_status_cells_v1 (
 item_key text not null references public.tara_mitzvah_status_items_v1(item_key),
 date_key text not null references public.tara_mitzvah_status_dates_v1(date_key),
 status text not null check(status in ('red','yellow','green')),
 updated_by uuid not null default auth.uid(), updated_at timestamptz not null default now(),
 primary key(item_key,date_key)
);
alter table public.tara_mitzvah_status_items_v1 enable row level security;
alter table public.tara_mitzvah_status_dates_v1 enable row level security;
alter table public.tara_mitzvah_status_cells_v1 enable row level security;
grant select on public.tara_mitzvah_status_items_v1,public.tara_mitzvah_status_dates_v1,public.tara_mitzvah_status_cells_v1 to anon,authenticated;
grant insert,update,delete on public.tara_mitzvah_status_cells_v1 to authenticated;
create policy tara_items_read on public.tara_mitzvah_status_items_v1 for select to anon,authenticated using(true);
create policy tara_dates_read on public.tara_mitzvah_status_dates_v1 for select to anon,authenticated using(true);
create policy tara_cells_read on public.tara_mitzvah_status_cells_v1 for select to anon,authenticated using(true);
create policy tara_cells_insert on public.tara_mitzvah_status_cells_v1 for insert to authenticated
 with check((select auth.uid())='bdfe3c81-3e96-4928-aa91-dc4ebabb7e87'::uuid and updated_by=(select auth.uid()));
create policy tara_cells_update on public.tara_mitzvah_status_cells_v1 for update to authenticated
 using((select auth.uid())='bdfe3c81-3e96-4928-aa91-dc4ebabb7e87'::uuid)
 with check((select auth.uid())='bdfe3c81-3e96-4928-aa91-dc4ebabb7e87'::uuid and updated_by=(select auth.uid()));
create policy tara_cells_delete on public.tara_mitzvah_status_cells_v1 for delete to authenticated
 using((select auth.uid())='bdfe3c81-3e96-4928-aa91-dc4ebabb7e87'::uuid);
insert into public.tara_mitzvah_status_items_v1 select item_key,label,sort_order from public.mitzvah_status_items_v1 where sort_order<=12;
insert into public.tara_mitzvah_status_items_v1
 select 'torah-'||n,'Torah · '||n,12+n from generate_series(1,15)n
 union all select 'script-'||n,'Script · '||n,27+n from generate_series(1,15)n;
insert into public.tara_mitzvah_status_items_v1
 select item_key,label,sort_order-2 from public.mitzvah_status_items_v1 where item_key ~ '^haftorah-[0-9]+$';
insert into public.tara_mitzvah_status_dates_v1
 select to_char(d,'MM-DD'),to_char(d,'FMMM/FMDD'),row_number() over(order by d)::integer
 from generate_series('2026-10-26'::date,'2027-01-04'::date,'7 days')d;
insert into public.tara_mitzvah_status_dates_v1 values('01-05','1/5',12);
notify pgrst,'reload schema';
