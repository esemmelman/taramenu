insert into public.tara_mitzvah_status_items_v1(item_key,label,sort_order)
select 'aliyah-'||n,'Aliyah '||n,17+n from generate_series(1,6) n
union all
select 'haftarah-'||n,'Haftarah '||n,23+n from generate_series(1,3) n
on conflict(item_key) do update set label=excluded.label,sort_order=excluded.sort_order
returning item_key,label,sort_order;
