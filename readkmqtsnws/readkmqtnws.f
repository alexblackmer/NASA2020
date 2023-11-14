
             program readkmqt


c nx > 144 10 minute intervals in day 
c ny = number of pixels
c nz = number of relationships
c na = number of events

             parameter(nx=200,ny=9,nz=4,na=1)

             real sr(nz,ny),sl(nz,ny),sm(nz,ny)
             real zr(ny),zl(ny),zm(ny)
             real acoeff(nz)
             character*50 infile,infile2,infile3
             character*50 inf0,out0,out2
             Character*50 out3,out4,out5,out6

             data acoeff/0.0102,0.0136,0.017,0.0476/
           
             open(9,file='filekmqtnws',status='unknown')
c starts do loop for each event
             do m=1,na
      
             read(9,10)it,inf0,out0
 10          format(i2,1x,a11,1x,a22)
c prints line
c             print*,inf0

c opens input file assigned to 10 and rthe same for 20
             open(10,file=inf0,status='unknown')
             open(20,file=out0,status='unknown')


             do ii=1,it
c 10 is the above opened file, while 20 is the format
             read(10,20)infile,infile2,infile3
 20          format(a43,1x,a43,1x,a43)

c opens kmqt/KMQT files
             open(11,file=infile,status='unknown')
             open(12,file=infile2,status='unknown')
             open(13,file=infile3,status='unknown')

c reads to nothing for first 12 lines
             do i=1,12
             read(11,*)
             read(12,*)
             read(13,*)
             enddo

             do i=1,nx
c zr, zl, zm are reflectivity at 0, 1, 2 elev            
             read(11,32,end=999)iy,mon,iday,ka,ma,isec,
     *       (zr(kl),kl=1,ny)
             read(12,33,end=999)idate,itime,(zl(kl),kl=1,ny)
             read(13,33,end=999)idate,itime,(zm(kl),kl=1,ny)
 32          format(3i2,3x,3i2,38x,9f8.2)
 33          format(i6,3x,i6,38x,9f8.2)

             if(iy.eq.17)iyear=2017
             if(iy.eq.18)iyear=2018

c reads only the cz 
             do kk=1,9
             read(11,*,end=999)
             read(12,*,end=999)
             read(13,*,end=999)
             enddo

             do kl=1,ny
c initializes array of -99.99
                     do kk=1,nz
                     sr(kk,kl)=-99.99
                     sl(kk,kl)=-99.99
                     sm(kk,kl)=-99.99
                     enddo
c applies all good pixel values with z-s and linear rel
                     if(zr(kl).gt.-90.)then
                        zmmr=10.**(zr(kl)/10.)
                        do kk=1,nz
                                sr(kk,kl)=acoeff(kk)*(zmmr**0.714)
                        enddo
                     endif
                     if(zl(kl).gt.-90.)then
                        zmml=10.**(zl(kl)/10.)
                        do kk=1,nz
                                sl(kk,kl)=acoeff(kk)*(zmml**0.714)
                        enddo
                     endif
                     if(zm(kl).gt.-90.)then
                        zmmm=10.**(zm(kl)/10.)
                        do kk=1,nz
                                sm(kk,kl)=acoeff(kk)*(zmmm**0.714)
                        enddo
                     endif
             enddo
c checks if middle pixel of 1st elev is bad
             if(zr(5).lt.-90.)then
                isay=0
                zsum=0
                jsay=0
                ztop=0.
c averages the adjacent pixels of 1st elev
                if(zr(2).gt.-90)then         
                        isay=isay+1
                        zsum=zsum+(10.**(zr(2)/10.))
                endif
                if(zr(4).gt.-90.)then
                        isay=isay+1
                        zsum=zsum+(10.**(zr(4)/10.))
                endif
                if(zr(6).gt.-90)then         
                        isay=isay+1
                        zsum=zsum+(10.**(zr(6)/10.))
                endif
                if(zr(8).gt.-90.)then
                        isay=isay+1
                        zsum=zsum+(10.**(zr(8)/10.))
                endif
                if(isay.gt.0)then
                        zmmave=zsum/float(isay)
                        do kk=1,nz
                                sr(kk,5)=acoeff(kk)*(zmmave**0.714)
                        enddo
checks middle pixel of 2nd elev
                elseif(zl(5).gt.-90.)then
                        zmml=10.**(zl(5)/10.)
                        do kk=1,nz
                                sr(kk,5)=acoeff(kk)*(zmml**0.714)
                        enddo
                else
c if not, summation of adjacent pixels of 2nd elev
                if(zl(2).gt.-90)then         
                        jsay=jsay+1
                        ztop=ztop+(10.**(zl(2)/10.))
                endif
                if(zl(4).gt.-90.)then
                        jsay=jsay+1
                        ztop=ztop+(10.**(zl(4)/10.))
                endif
                if(zl(6).gt.-90)then         
                        jsay=jsay+1
                        ztop=ztop+(10.**(zl(6)/10.))
                endif
                if(zl(8).gt.-90.)then
                        jsay=jsay+1
                        ztop=ztop+(10.**(zl(8)/10.))
                endif
                if(jsay.gt.0.)then
                        zmmav=ztop/float(jsay)
                        do kk=1,nz
                                sr(kk,5)=acoeff(kk)*(zmmav**0.714)
                        enddo
                endif
             endif
             endif
c output gives middle pix(5) for each z-s and each elev           
             if(mon.eq.1)jday=iday
             if(mon.eq.2)jday=iday+31
             if(mon.eq.3)jday=iday+59
             if(mon.eq.4)jday=iday+90
             if(mon.eq.12)jday=iday+334
             write(20,34)iyear,jday,ka,ma,isec,(sr(kk,5),kk=1,nz),
     *       (sl(kk,5),kk=1,nz),(sm(kk,5),kk=1,nz)
 34          format(5i5,15f10.2)



 999         enddo

             enddo

             enddo

             stop
             end

