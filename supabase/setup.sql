-- Mallu's Design Tool: pilvitallennuksen taulut ja suojaukset
-- Aja tämä Supabasessa: SQL Editor -> New query -> liitä -> Run

-- Projektit: jokainen käyttäjä näkee ja muokkaa vain omiaan
create table if not exists public.projects (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  name text not null default 'Nimetön',
  data jsonb not null,
  updated_at timestamptz not null default now()
);
create index if not exists projects_user_idx on public.projects(user_id, updated_at desc);

alter table public.projects enable row level security;
grant select, insert, update, delete on public.projects to authenticated;

drop policy if exists "omat projektit: luku" on public.projects;
drop policy if exists "omat projektit: lisäys" on public.projects;
drop policy if exists "omat projektit: muokkaus" on public.projects;
drop policy if exists "omat projektit: poisto" on public.projects;
create policy "omat projektit: luku" on public.projects for select to authenticated using (user_id = (select auth.uid()));
create policy "omat projektit: lisäys" on public.projects for insert to authenticated with check (user_id = (select auth.uid()));
create policy "omat projektit: muokkaus" on public.projects for update to authenticated using (user_id = (select auth.uid())) with check (user_id = (select auth.uid()));
create policy "omat projektit: poisto" on public.projects for delete to authenticated using (user_id = (select auth.uid()));

-- Kuvat (pohjakuvat, valokuvat, panoraamat): yksityinen säiliö, jokaisella oma kansio
insert into storage.buckets (id, name, public) values ('images', 'images', false)
on conflict (id) do nothing;

drop policy if exists "omat kuvat: luku" on storage.objects;
drop policy if exists "omat kuvat: lisäys" on storage.objects;
drop policy if exists "omat kuvat: poisto" on storage.objects;
create policy "omat kuvat: luku" on storage.objects for select to authenticated
  using (bucket_id = 'images' and (storage.foldername(name))[1] = (select auth.uid())::text);
create policy "omat kuvat: lisäys" on storage.objects for insert to authenticated
  with check (bucket_id = 'images' and (storage.foldername(name))[1] = (select auth.uid())::text);
create policy "omat kuvat: poisto" on storage.objects for delete to authenticated
  using (bucket_id = 'images' and (storage.foldername(name))[1] = (select auth.uid())::text);
