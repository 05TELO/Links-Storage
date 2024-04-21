SELECT u.id, u.email , Count(l.id) AS links_amount,
  SUM(case l.link_type when 'website' then 1 else 0 end) as website,
  SUM(case l.link_type when 'book' then 1 else 0 end) as book,
  SUM(case l.link_type when 'article' then 1 else 0 end) as article,
  SUM(case l.link_type when 'music' then 1 else 0 end) as music,
  SUM(case l.link_type when 'video' then 1 else 0 end) as video
FROM api_customuser AS u
LEFT JOIN api_link AS l
ON u.id = l.user_id
GROUP BY u.id
ORDER BY links_amount DESC, u.date_joined ASC
LIMIT 10;