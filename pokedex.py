from helper import *

async def run_pokedex(ctx, name='broken', gen='0', extra='0'):
    try:
        name = name.lower()
        gen = gen.lower()
        approved_file = open('text/approved.txt','r')
        approved = approved_file.readlines()
        approved_file.close()
        # Adds a new user to the approved list
        if name=='register':
            if gen+'\n' in approved:
                await ctx.send(gen.title()+' has already been approved')
                return

            new_dex = open('text/'+gen+'_dex.txt','w')
            new_dex.close()
            new_approved = open('text/approved.txt','a')
            new_approved.write(gen+'\n')
            new_approved.close()
            await ctx.send(gen.title()+' has been approved!')
            
        # Outputs what <arg1> needs with the option to restrict the generation
        elif gen=='0' or gen=='1' or gen=='2' or gen=='3':
            if not (((name+'\n') in approved) or name=='both'):
                await ctx.send(name.title()+' is not a valid user')
                return

            need = open('text/'+name+'_need.txt','w')
            if gen=='0':
                dex1 = open('text/pokedex_gen1.txt','r')
                dex2 = open('text/pokedex_gen2.txt','r')
                dex3 = open('text/pokedex_gen3.txt','r')
                dex = [dex1, dex2, dex3]
            else:
                dex1 = open('text/pokedex_gen'+gen+'.txt','r')
                dex = [dex1]

            if name=='both':
                ty_dex = open('text/ty_dex.txt','r')
                brian_dex = open('text/brian_dex.txt','r')
                ty_cont = ty_dex.readlines()
                brian_cont = brian_dex.readlines()
                check = [ty_cont, brian_cont]
                ty_dex.close()
                brian_dex.close()
                addition = ''
            else:
                check_dex = open('text/'+name+'_dex.txt','r')
                cont = check_dex.readlines()
                check = [cont]
                check_dex.close()
                addition = 's'

            for i in range(len(dex)):
                if len(dex)>1:
                    need.write('@@@@@@@@@@ GEN '+str(i+1)+' @@@@@@@@@@\n')
                for line in dex[i]:
                    if len(check)==2:
                        if not ((line in check[0]) or (line in check[1])):
                            if 'mr. mime' in line:
                                need.write('Mr. Mime\n')
                            else:
                                need.write(line.title())
                    else:
                        if not (line in check[0]):
                            if 'mr. mime' in line:
                                need.write('Mr. Mime\n')
                            else:
                                need.write(line.title())
                dex[i].close()
            need.close()

            need = open('text/'+name+'_need.txt','r')

            await ctx.send(name.title()+' still need'+addition+':')
            read = need.read()
            need.close()
            if(len(read)==0):
                await ctx.send('Nothing! You got all of them!')
            else:
                await ctx.send(read)

        # Adds <arg2> to <arg1>s pokedex
        else:
            if not ((name+'\n') in approved):
                await ctx.send(name.title()+' is not a valid user')
                return

            if extra != '0':
                gen = gen + ' ' + extra

            dex1 = open('text/pokedex_gen1.txt','r')
            dex2 = open('text/pokedex_gen2.txt','r')
            dex3 = open('text/pokedex_gen3.txt','r')
            dex = [dex1, dex2, dex3]

            pokemon = (gen+'\n')

            valid = False

            for i in range(len(dex)):
                if pokemon in dex[i]:
                    valid = True
                    break

            if valid:
                check_dex = open('text/'+name+'_dex.txt','r')
                check = check_dex.readlines()
                check_dex.close()

                if pokemon not in check:
                    file = open('text/'+name+'_dex.txt','a')
                    file.write(pokemon)
                    file.close()
                    await ctx.send(pokemon.title().rstrip()+' has been succesfully added!')
                else:
                    await ctx.send(pokemon.title().rstrip()+' is already in '+name.title()+'\'s Pokedex')

            else:
                await ctx.send(pokemon.title().rstrip()+' is not a valid Pokemon')

    except:
        await ctx.send('use \'/help pokedex\'')
        raise