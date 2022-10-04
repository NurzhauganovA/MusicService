
CREATE OR REPLACE PROCEDURE hello_time (
    p_message out VARCHAR2) 
IS
    now_time VARCHAR(50);
    
BEGIN
    now_time := to_char(sysdate,'HH24MI');
    IF now_time >= 0601 AND now_time <= 1200 THEN
        p_message := 'Good morning';
    ELSIF now_time >= 1201 AND now_time <= 1800 THEN
        p_message := 'Good day';
    ELSIF now_time >= 1801 AND now_time <= 2300 THEN
        p_message := 'Good evening';
    ELSE 
        p_message := 'Good night';
    END IF;
END;


CREATE OR REPLACE PROCEDURE sorted_albums (
    p_bool in number) 
IS
    cursor_albums sys_refcursor;
    
BEGIN
    IF p_bool = 1  THEN
        open cursor_albums for SELECT ID ,
                                IMG ,
                                NAME_OF_ALBUM ,
                                "DATE" ,
                                SLUG ,
                                AUTHOR_OF_ALBUM_ID 
                            FROM MUSIC_ALBUM 
                            ORDER BY MUSIC_ALBUM."DATE" DESC;
        dbms_sql.return_result(cursor_albums);
    ELSE 
        DBMS_OUTPUT.PUT_LINE('WE DONT HAVE ANY ALBUMS');
    END IF;
END;

DECLARE
    v_id number;
BEGIN
    v_id := 0;
    sorted_albums(v_id);
END;


CREATE OR REPLACE PROCEDURE liked_musics (
    p_id in number) 
IS
    cursor_likes sys_refcursor;
    
BEGIN
        open cursor_likes for SELECT MUSIC_ID     
                            FROM MUSIC_MUSIC_LIKE_MUSIC
                            WHERE CUSTOMUSER_ID = p_id;
        dbms_sql.return_result(cursor_likes);
    
END;

DECLARE
    v_id number;
BEGIN
    v_id := 1;
    liked_musics(v_id);
END;


CREATE OR REPLACE FUNCTION sum_likes (
    p_author_id NUMBER)
RETURN number IS
 
 sum_like NUMBER := 0;
 
 CURSOR cursor_liked_author IS
   SELECT lm.id, m.author_name_id
    FROM music_music_like_music lm
    JOIN music_music m
    ON lm.music_id = m.id;
    
 temp1 cursor_liked_author%rowtype;
BEGIN
  OPEN cursor_liked_author;
  LOOP
    FETCH cursor_liked_author INTO temp1;
    IF temp1.author_name_id = p_author_id  THEN
        sum_like := sum_like + 1;
    END IF;
    EXIT WHEN cursor_liked_author%NOTFOUND;
  END LOOP;
  CLOSE cursor_liked_author;
    RETURN sum_like;
END;


DECLARE
    v_author_id number;
BEGIN
    v_author_id := 1;
    dbms_output.put_line(sum_likes(v_author_id));
END;

