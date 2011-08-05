# coding=UTF-8
from __future__ import division
from bellum.space.models import Planet
import Image, ImageFont, ImageDraw
import aggdraw
print('Henrietta: Bellum Suite v0.1')
print 'Call generate_universe() for uni generation'
print '> May take an hour even on fast equipment!'
print 'Call expand_planetview_icons() for planet view icons generation'
print 'Call expand_sectors() for sectors and regions generation'
print 'Call regenerate_rankings_psn() to regenerate personal rankings'
print 'Call regenerate_rankings_all() to regenerate alliance rankings'


def regenerate_rankings_psn():
    from bellum.suite.ranking import regen_personal_ranking
    regen_personal_ranking()

def regenerate_rankings_all():
    from bellum.suite.ranking import regen_allied_ranking
    regen_allied_ranking()

def expand_sectors():
    mini_c = -500
    worldres = 1000
    # expand galaxy
    print '> Expanding galaxy...'
    secmap = []
    for i in xrange(0, 10):    # Make... 100 images
        secmap.append(map(lambda x: Image.new('RGB', (84, 84), (1, 8, 18)), range(0, 10)))
    def plot_gal(secmap, x, y, kind):
        kindc = {0: (0, 255, 0), 1:(255,0,0), 2:(0,0,255)}
        x, y = x - mini_c, y - mini_c
        mx, my = x % 100, y % 100
        mx, my = mx*0.84, my*0.84
        x, y = x // 100, y // 100
        secmap[x][y].putpixel((int(mx), int(my)), kindc[kind])
    for p in Planet.objects.all():
        plot_gal(secmap, p.x, p.y, p.kind)
    for x in xrange(0, 10):
        for y in xrange(0, 10):
            secmap[x][y].save('media/sector_images/g'+str(x)+'-'+str(y)+'.png', "PNG")
        print '>> '+str(x)+'0 %'
    print '>> 100%'

    # expand sectors
    print '> Expanding sectors...'
    secmap = []
    for i in xrange(0, 50):    
        secmap.append(map(lambda x: Image.new('RGB', (56, 56), (1, 8, 18)), range(0, 50)))

    def plot_planet(secmap, x, y, kind):
        kindc = {0: (0, 255, 0), 1:(255,0,0), 2:(0,0,255)}
        x, y = x - mini_c, y - mini_c
        mx, my = x % 20, y % 20
        mx, my = int(mx * 2.8), int(my * 2.8)
        x, y = x // 20, y // 20
        secmap[x][y].putpixel((mx+0, my+0), kindc[kind])
        secmap[x][y].putpixel((mx+1, my+0), kindc[kind])
        secmap[x][y].putpixel((mx+0, my+1), kindc[kind])
        secmap[x][y].putpixel((mx+1, my+1), kindc[kind])

    for p in Planet.objects.all():
        plot_planet(secmap, p.x, p.y, p.kind)

    for x in xrange(0, 50):
        for y in xrange(0, 50):
            secmap[x][y].save('media/sector_images/s'+str(x)+'-'+str(y)+'.png', "PNG")
        print '>> '+str(x*2)+' %'
    print '>> 100%'
   

def expand_planetview_icons():
    font = ImageFont.truetype('suite/arial.ttf',size=16)

    for num in xrange(1, 18):
        for color in ('red', 'blue', 'green', 'yellow', 'gray'):
            for highlight in (True, False):
                bi = Image.open('suite/'+color+'.png')
                bd = ImageDraw.Draw(bi)
                if num < 10:
                    bd.text((9,4),str(num),font=font,fill='#ffffff')
                else:
                    bd.text((3,4),str(num),font=font,fill='#ffffff')
                
                if highlight:
                    highlight = Image.open('suite/highlight.png')
                    highlight.paste(bi, (6,6), bi)
                    add='h'
                else:
                    highlight = Image.new('RGBA', (38,39), (0,0,0,0))
                    highlight.paste(bi, (6,6))
                    add = ''
                                    
                highlight.save('media/planet_images/'+color+str(num)+add+'.png','PNG')

def generate_universe():
    print('Ressourcen initializieren...')
    from suite.ringgen import generate, RingDefinition, sumup
    from suite.mathops import polar_to_cartesian, polarcs_distance, do_segments_intersect, minmax, distance, getStandarizedGauss
    from random import choice, shuffle
    from suite.namegen import getName
    worldres = 1000
    print('Aufloesung des Weltes an '+str(worldres)+'x'+str(worldres)+' eingesteld')
    print('Welt bilden...')
    print('> Koordinaten bilden...')
    rings = [RingDefinition(0.8, 0.2, 0.04),
             RingDefinition(0.4, 0.2, 0.3),
             RingDefinition(0.1, 0.1, 1)]

    rings = map(lambda x: generate(worldres//2, worldres//2, x), rings)

    print('> Mit Probablistik Planetklass verarbeiten...')

    generationprobablistik = ((0.2375, 0.7125, 0.05),
                              (0.3, 0.5, 0.2),
                              (0.2, 0.4, 0.4))

    from random import random
    def probablistikKlass(pklass):
        r = random()
        if r < pklass[0]:
            return 0
        if r < pklass[0]+pklass[1]:
            return 1
        return 2

    rk = []
    klassgen = 0
    for ring in rings:
        for kx, v in ring.iteritems():
            for ky, y in v.iteritems():
                rk.append((kx, ky, probablistikKlass(generationprobablistik[klassgen])))
        klassgen += 1

    print('> Verbinden...')
    print str(len(rk))+' Total'
    print str(len(filter(lambda x: x[2]==0, rk)))+' Startenplanetklass'
    print str(len(filter(lambda x: x[2]==1, rk)))+' Normalplanetklass'
    print str(len(filter(lambda x: x[2]==2, rk)))+' Himmelplanetklass'
    print('Lande bilden...')
    #from bellum.space.models import Planet
    #from bellum.province.models import Province
    def pkogen(maxprovinz):
        MAPSIZE = 100       # This is only half of the map!
        MINDIST = 60-maxprovinz*2
        provinzes = []
        failed_attempts = 0
        while failed_attempts < 50:
            prov = (random()*(MAPSIZE-MINDIST//2), random()*360)
            try:
                for pt in provinzes:
                    if polarcs_distance(prov[0], prov[1], pt[0], pt[1]) < MINDIST:
                        failed_attempts += 1
                        raise Exception
            except:
                continue
            failed_attempts = 0
            provinzes.append(prov)
            if len(provinzes) == maxprovinz:
                break
        provinzes = map(lambda x: polar_to_cartesian(*x), provinzes)
        provinzes = map(lambda x: (int(x[0]), int(x[1])), provinzes)
        return provinzes


    def createImage(provlist, pathes, index):
        img = Image.open('suite/planet.png')
        draw = aggdraw.Draw(img)
        draw.setantialias(True)
        pen = aggdraw.Pen("#002640", 3)

        def scales(x, y, size):
            return int((x+100) * (size[0])/200), int((y+100) * (size[1])/200)

        for path in pathes:
            p1, p2 = path
            xy1, xy2 = provlist[p1], provlist[p2]
            x1, y1 = scales(xy1[0], xy1[1], img.size)
            x2, y2 = scales(xy2[0], xy2[1], img.size)
            draw.line((x1, y1, x2, y2), pen)
        draw.flush()

        img.save('media/planet_images/'+str(index)+'.png', "PNG")

    #    for i in xrange(0, len(provlist)):
    #        x, y = provlist[i]
    #        draw.ellipse((x+80, y+80, x+120, y+120))
    #        draw.text((x+100, y+100), str(i), fill=(255, 255, 255))

    def trackgen(provlist):                 # FUKKEN MAGIC. Do not read sober.
        pathes = []     # current pathes list
        # Enumerate possible pathes
        ppathes = []
        for ix in xrange(0, len(provlist)):
            for iy in xrange(0, len(provlist)):
                if ix == iy: continue
                mmx = minmax(ix, iy)
                if mmx in ppathes:
                    continue
                ppathes.append(minmax(ix, iy))
        # Ok, now run len(provlist)-1 iterations of shortest-find
        # We're pretty much guaranteed to find that stuff
        for iteratee in xrange(0, len(provlist)-1):
            shortest_p = None
            shortest_v = 1000
            for p in ppathes:
                p1, p2 = p
                x1, y1 = provlist[p1]
                x2, y2 = provlist[p2]
                d = distance(x1, y1, x2, y2)
                if d < shortest_v:
                    # Its one of the shorter ones, so check for collisions...
                    intersection_found = False
                    for cp1, cp2 in pathes:
                        cpx1, cpy1 = provlist[cp1]
                        cpx2, cpy2 = provlist[cp2]
                        if do_segments_intersect(x1, y1, x2, y2, cpx1, cpy1, cpx2, cpy2):
                            intersection_found = True
                            break
                    if intersection_found:
                        continue
                    shortest_p = p
                    shortest_v = d
            if shortest_p == None:
                break                   # WE'VE JUST FAILED MISERABLY
            # ok, shortest_p is the shortest path...
            ppathes.remove(shortest_p)
            pathes.append(shortest_p)

        # Ok, now run those iterations until graph is connected...
        while True:
            # Check whether the graph is connected!
            current_nodes = [0]
            is_connected = False
            for iteratee2 in xrange(0, len(provlist)):      # Just run n times...
                nodepath = []
                for current_node in current_nodes:
                    for fv in pathes:
                        a, b = fv
                        if a == current_node: nodepath.append(b)
                        if b == current_node: nodepath.append(a)
                # Uniquefy nodepath
                nodepath_t = {}
                for x in nodepath:
                    nodepath_t[x] = 1
                nodepath = list(nodepath_t.keys())

                roundup_test = True
                for nodename in range(0, len(provlist)):
                    if not (nodename in nodepath):
                        roundup_test = False
                        break
                if not roundup_test:
                    continue

                is_connected = True
                break
            if is_connected:
                break
            shortest_p = None
            shortest_v = 1000
            for p in ppathes:
                p1, p2 = p
                x1, y1 = provlist[p1]
                x2, y2 = provlist[p2]
                d = distance(x1, y1, x2, y2)
                if d < shortest_v:
                    # Its one of the shorter ones, so check for collisions...
                    intersection_found = False
                    for cp1, cp2 in pathes:
                        cpx1, cpy1 = provlist[cp1]
                        cpx2, cpy2 = provlist[cp2]
                        if do_segments_intersect(x1, y1, x2, y2, cpx1, cpy1, cpx2, cpy2):
                            intersection_found = True
                            break
                    if intersection_found:
                        continue
                    shortest_v = d
                    shortest_p = p
            if shortest_p == None:
                break
            # ok, shortest_p is the shortest path...
            ppathes.remove(shortest_p)
            pathes.append(shortest_p)
        return pathes

    nrk = []
    for i in xrange(0, len(rk)):
        x, y, klass = rk[i]
        provinzgran = {0: (5,6),
                       1: (5,8),
                       2: (3,4)}
        while True:
            min, max = provinzgran[klass]
            pk = pkogen(choice(provinzgran[klass]))
            if (len(pk) <= max) and (len(pk) >= min):
                break
        ts = trackgen(pk)
        nrk.append((x, y, klass, pk, ts))

    print 'Datenbankobjekte bilden und speichern...'
    from bellum.space.models import Planet, LinkingSetter
    from bellum.province.models import Province
    replist = []
    minicounter = 0
    for _p in nrk:
        x, y, klass, pk, ts = _p
        p = Planet(x=x,
                   y=y,
                   name=getName(),
                   kind=klass,
                   path_graph=0,     # Will generate later
                   kustomization=0,     # So far unused
                   amount_of_provinces=len(pk))
        p.save()
        cpls = LinkingSetter(p, len(pk))
        for cn in ts:
            #p.path_graph += (1 << _getLinkBit(*cn))
            cpls.set(*cn)
        del cpls        # explicitly destroy object - destructor saves data
                        # good programming practice, to avoid magic, is

        replist.append((klass, p, pk, ts))
        createImage(pk, ts, p.id)
        # Prepare no of connections for provinces...
        num_of_connections = {}
        for a, b in ts:
            try:
                num_of_connections[a] += 1
            except:
                num_of_connections[a] = 1
            try:
                num_of_connections[b] += 1
            except:
                num_of_connections[b] = 1

        for provid in xrange(0, len(pk)):
            x, y = pk[provid]
            pname = p.name+' '+str(provid+1)
            if klass == 0:
                town_coef = 0.9+random()*0.2
                titan_coef = 0.9+random()*0.2
                pluton_coef = 0.9+random()*0.2
                slots=3
                natural_defense_level = 0.2 + random()*0.1
            if klass == 1:
                town_coef, titan_coef, pluton_coef = 0, 0, 0
                if random() > 0.4:
                    town_coef = 1+1.5*abs(getStandarizedGauss())
                if random() > 0.4:
                    titan_coef = 1+1.5*abs(getStandarizedGauss())
                if random() > 0.4:
                    pluton_coef = 1+1.5*abs(getStandarizedGauss())
                slots=3
                natural_defense_level = -0.5 + abs(getStandarizedGauss())
            if klass == 2:
                town_coef, titan_coef, pluton_coef = 0, 0, 0
                if random() > 0.6:
                    town_coef = 3+3*abs(getStandarizedGauss())
                if random() > 0.6:
                    titan_coef = 3+3*abs(getStandarizedGauss())
                if random() > 0.6:
                    pluton_coef = 3+3*abs(getStandarizedGauss())
                slots = 3

                natural_defense_level = getStandarizedGauss()/0.5 + 0.2
            natural_defense_level += 1      # for it to be <0; 1>


            town_coef *= (num_of_connections[provid]-1)/10 + 1
            pluton_coef *= (num_of_connections[provid]-1)/10 + 1
            titan_coef *= (num_of_connections[provid]-1)/10 + 1

            Province(x=x, y=y, planet_count_number=provid, name=pname, town_coef=town_coef, titan_coef=titan_coef, pluton_coef=pluton_coef,
                                slots=slots,
                                natural_defense_level=natural_defense_level, planet=p).save()

        minicounter += 1
        if (minicounter % 10) == 0:
            print ' >> '+str(minicounter)+' mark'

    print 'Neuespielerallokatorlist bilden...'

    replist = filter(lambda x: x[0]==0, replist)        # Get only startplanets
    replist = map(lambda x: x[1], replist)             # Only planet DBO
    rcf = {}
    for planet in replist:
        try:
            rcf[planet.y].append(planet)
        except:
            rcf[planet.y] = [planet]

    print '> Speichern...'
    plist = []
    for dy in xrange(-worldres//2, worldres//2+1):
        if not rcf.has_key(dy): continue
        for planet in rcf[dy]:
            plist.append(planet)

    open('planetlist.nsal', 'w').write(repr(map(lambda x: x.id,plist[1:])))
    open('allocatorstatus.nsal','w').write('('+str(plist[0].id)+', None, 0)')
    print 'OK'