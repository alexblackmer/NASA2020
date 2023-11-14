
               program radarrate

               Parameter(nx=2000,ny=4,nr=1)
               Parameter(nn=3)
c number of z-s rel, nr number of events, nx is 10 min increments, nn is
3 elev
               Integer jday(nx),ka(nx),ma(nx),isec(nx)

               Real precip(nx,ny,nn),time(nx),psave(ny,nn)
               Real ptotal(ny,nn)
               character*40 infile,outfile,outfile2
           

               open(10,file='filepratenws',status='unknown')
               open(12,file='fileevent_dbz',status='unknown')
               open(22,file='pl01_nws_ptotal.kmqt',status='unknown')

               do ii=1,nr
c julian daym number of days etc
                        read(10,19)jdy,it,infile,outfile,outfile2
 19                     format(i3,1x,i2,1x,a22,1x,a28,1x,a29)
c js is julian day, ks jul starting hr, je is end julian day, ke end
hour
                        read(12,*)jyear,js,ks,je,ke
c converts julian day hr to numerical day
                        timeb=float(js)+float(ks)/24.
                        timee=float(je)+float(ke+1)/24.
c opens files
                        open(11,file=infile,status='unknown')
                        open(20,file=outfile,status='unknown')
                        open(21,file=outfile2,status='unknown')


                        k1=1
                         do i=1,nx
c reads previously generated file
                                read(11,*,end=999)iyear,jday(k1),ka(k1),ma(k1),isec(k1),
c nn is 3 because 3 altitudes, ny is 4 relationships
                                ((precip(k1,k,kk),k=1,ny),kk=1,nn)
c               converts to partial day
                                time0=float(ma(k1))+float(isec(k1))/60.
                                time1=time0/60.+float(ka(k1))
                                time(k1)=time1/24.+float(jday(k1))
c shows number of rows k1
                                k1=k1+1
 999                      enddo
c subbed to represent hour and make up for k1 = 1
                          k1=k1-1

                          do kl=1,ny
                                do kh=1,3
                                        ptotal(kl,kh)=0.
                                enddo
                          enddo
c dif is the 10 min fraction of a day
                          dif=(10./60.)/24.
c reads julian day from file
                          jd=jdy
c it is how man days, kr is hour 0
                          do i=1,it
                                kr=0
                                do j=1,24
c minute 0 is mn
                                        mn=0
                                        do l=1,60
c making partial hour and day
                                                times=float(mn)/60.+float(kr)
                                                times=times/24.+float(jd)
                                                tdifsave=1.
                                                do k=1,k1
c difference between radar scan(timeK)
c finding corresponding radar scan for a 1 min time period
c times is the time corresonding to radar data
                                                        tdif=abs(times-time(k))
                                                        tdif1=abs(times-time(k+1))
                                                        if(tdif.lt.dif .and. tdif.lt.tdifsave
                                              *         .and. tdif .lt.tdif1)then
                                                                do kl=1,ny
c for each z-s rel and elev
                                                                        do kh=1,3
                                                                             psave(kl,kh)=precip(k,kl,kh)
                                                                             if(precip(k,kl,kh).gt.0.)then
c between beginina and end time
                                                                                    if(times .ge.timeb .and. times .le. timee)then
c /60 converts from  mm/hr to mm
                                                                                             ptotal(kl,kh)=ptotal(kl,kh)+precip(k,kl,kh)/60.
                                                                                    endif
                                                                             endif
                                                                        enddo
                                                                enddo
                                                                tdifsave=tdif
                                                        endif
                                                enddo
                                                write(20,12)iyear,jd,kr,mn,((psave(kl,kh),kl=1,ny),kh=1,nn)
                                                write(21,12)iyear,jd,kr,mn,((ptotal(kl,kh),kl=1,ny),kh=1,nn)
 12                                             format(4i5,15f10.2)
                                                mn=mn+1
                                        enddo
                                        kr=kr+1
                                enddo
                                jd=jd+1
                          enddo
                          do kh=1,3
c ptotal is the accumulated precip over each even for a given zs rel and elevt
                                write(22,13)iyear,jdy,(ptotal(kl,kh),kl=1,ny)
 13                             format(2i5,15f10.2)
                          enddo

               enddo

               stop
               end
