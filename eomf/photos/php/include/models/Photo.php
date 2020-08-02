<?
/*
REATE TRIGGER auto_geom BEFORE INSERT OR UPDATE ON photos FOR EACH ROW EXECUTE PROCEDURE make_geom()
CREATE or replace FUNCTION make_geom () RETURNS trigger as
 $BODY$
 BEGIN
 NEW.point := SetSRID(makepoint(NEW.long, NEW.lat), 4326);
 RETURN NEW;
 END
 $BODY$
LANGUAGE plpgsql;
*/

class Photo extends ActiveRecord\Model {

    static $belongs_to = array(
        array('category', 'foreign_key'=>'categoryid')
        array('user', 'foreign_key'=>'userid'),
    );

    static $validates_length_of = array(
        array('location', 'within' => array(1,128)),
        array('source', 'within' => array(1,100))
    );
    
    static $validates_presence_of = array(
        array('location')
    );
    
}

?>
