begin;
-- Retain the four blessing rows and their stable keys.
-- Foreign keys prevent deletion of an item if progress has since been saved.
delete from public.tara_mitzvah_status_items_v1
where item_key not in ('torah-blessing-before','torah-blessing-after','haftorah-blessing-before','haftorah-blessing-after');

-- Move retained rows away from the new service-page positions.
update public.tara_mitzvah_status_items_v1 set sort_order=sort_order+1000;

insert into public.tara_mitzvah_status_items_v1(item_key,label,sort_order)
select 'service-page-'||n,'Page '||n,n from generate_series(1,13) n;

update public.tara_mitzvah_status_items_v1
set sort_order=case item_key
 when 'torah-blessing-before' then 14
 when 'torah-blessing-after' then 15
 when 'haftorah-blessing-before' then 16
 when 'haftorah-blessing-after' then 17
end
where item_key in ('torah-blessing-before','torah-blessing-after','haftorah-blessing-before','haftorah-blessing-after');
commit;
