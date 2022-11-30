from treemap import *


# EXAMPLE utility file copied to assignment directory


smallMap = map_insert('one', \
                        1,  \
                        map_insert('two', \
                                     2,  \
                                     map_insert('three', 3, None)))


numberMap = map_insert(                                  \
   'seven',                                             \
      7,                                                \
      map_insert(                                        \
      'eight',                                          \
         8,                                             \
         map_insert(                                     \
         'two',                                         \
            2,                                          \
            map_insert(                                  \
            'six',                                      \
               6,                                       \
               map_insert(                               \
               'nine',                                  \
                  9,                                    \
                  map_insert(                            \
                  'five',                               \
                     5,                                 \
                     map_insert(                         \
                     'three',                           \
                        3,                              \
                        map_insert(                      \
                        'four',                         \
                           4,                           \
                           map_insert(                   \
                           'one',                       \
                              1,                        \
                              None)))))))))



def test(word, num, treemap):
    x = map_search(word, treemap)
    if x == num:
        print("PASS")
    else:
        print("FAIL")
        print(x)


def main():
    """
    print the tree above using map_to_str
    """
    
    test("three", 3, smallMap)
    test("ten", None, smallMap)
    test("seven", 7, numberMap)
    
    x = map_to_str(smallMap)
    
    if x == "'((_, one->1, _), three->3, (_, two->2, _))'" or x == "((_, one->1, _), three->3, (_, two->2, _))":
        print("PASS")
    else:
        print("FAIL")
        print(x)
        print("VS.")
        print("'((_, one->1, _), three->3, (_, two->2, _))'")
    


if __name__ == "__main__":
    main()
