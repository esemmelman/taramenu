-- Keep existing item keys to preserve any saved progress.
update public.tara_mitzvah_status_items_v1
set label = case item_key
  when 'haftorah-4' then 'Haftarah · Ezekiel 28:25'
  when 'haftorah-5' then 'Haftarah · Ezekiel 28:26'
  when 'haftorah-6' then 'Haftarah · Ezekiel 29:1'
end
where item_key in ('haftorah-4', 'haftorah-5', 'haftorah-6');
