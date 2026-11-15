-- Mallu's Design Tool: ylläpidon raportti (käyttäjämäärät)
-- 1) Aja tämä koko tiedosto SQL Editorissa.
-- 2) Kun olet kirjautunut sivulla kerran, aja alin rivi omalla sähköpostillasi.

create table if not exists public.admins (
  user_id uuid primary key references auth.users(id) on delete cascade
);
alter table public.admins enable row level security;
-- Ei sääntöjä: taulua ei voi lukea eikä muokata sivun kautta, vain hallintapaneelista.

create or replace function public.admin_stats()
returns json
language sql
security definer
set search_path = ''
as $$
  select case when exists (select 1 from public.admins a where a.user_id = auth.uid()) then
    json_build_object(
      'users',       (select count(*) from auth.users),
      'users_week',  (select count(*) from auth.users where created_at > now() - interval '7 days'),
      'active_week', (select count(*) from auth.users where last_sign_in_at > now() - interval '7 days'),
      'projects',    (select count(*) from public.projects),
      'latest',      (select coalesce(json_agg(x), '[]'::json) from (select email, created_at from auth.users order by created_at desc limit 5) x)
    )
  else null end
$$;
revoke all on function public.admin_stats() from public, anon;
grant execute on function public.admin_stats() to authenticated;

-- Tee itsestäsi ylläpitäjä (vaihda oma sähköpostisi):
-- insert into public.admins (user_id) select id from auth.users where email = 'oma@sahkoposti.fi';
