##---------------------------------------------------------------------------##
##
## pyChing -- a Python program to cast and interpret I Ching hexagrams
##
## Copyright (C) 1999,2000 Stephen M. Gava
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be of some
## interest to somebody, but WITHOUT ANY WARRANTY; without even the 
## implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
## See the GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; see the file COPYING or COPYING.txt. If not, 
##  write to the Free Software Foundation, Inc.,
## 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
## The license can also be found at the GNU/FSF website: http://www.gnu.org
##
## Stephen M. Gava
## <elguavas@users.sourceforge.net>
## http://pyching.sourgeforge.net
##
##---------------------------------------------------------------------------##
"""
a couple of classes for implementing partial tabbed-page like behaviour
"""

from Tkinter import *

class PageTab(Frame):
    """
    a 'page tab' like framed button
    """ 
    def __init__(self,parent):
        Frame.__init__(self, parent,borderwidth=2,relief=RIDGE)
        self.button=Radiobutton(self,padx=5,pady=5,takefocus=FALSE,
                underline=0,indicatoron=FALSE,highlightthickness=0,
                borderwidth=0,selectcolor=self.cget('bg'))
        self.button.pack()
      
class TabPageSet(Frame):
    """
    a set of 'pages' with TabButtons for controlling their display
    """ 
    def __init__(self,parent,pageNames,**kw):
        """
        pageNames - a list of strings, each string will be the dictionary key
        to a page's data, and the name displayed on the page's tab. Should be 
        specified in desired page order. The first page will be the default 
        and first active page.
        """
        Frame.__init__(self, parent, kw)
        self.grid_location(0,0)
        self.columnconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)
        self.tabBar=Frame(self)
        self.tabBar.grid(row=0,column=0,sticky=EW)
        self.activePage=StringVar(self)
        self.defaultPage=''
        self.pages={}
        for name in pageNames:
            self.AddPage(name)

    def ChangePage(self,pageName=None):
        if pageName:
            if pageName in self.pages.keys():
                self.activePage.set(pageName)
            else:
                raise 'Invalid TabPage Name'
        ## pop up the active 'tab' only
        for page in self.pages.keys(): 
            self.pages[page]['tab'].config(relief=RIDGE)
        self.pages[self.GetActivePage()]['tab'].config(relief=RAISED)
        ## switch page
        self.pages[self.GetActivePage()]['page'].lift()
        
    def GetActivePage(self):
        return self.activePage.get()

    def AddPage(self,pageName):
        if pageName in self.pages.keys():
            raise 'TabPage Name Already Exists'
        self.pages[pageName]={'tab':PageTab(self.tabBar),
                'page':Frame(self,borderwidth=2,relief=RAISED)}
        self.pages[pageName]['tab'].button.config(text=pageName,
                command=self.ChangePage,variable=self.activePage,
                value=pageName)
        self.pages[pageName]['tab'].pack(side=LEFT)
        self.pages[pageName]['page'].grid(row=1,column=0,sticky=NSEW)
        if len(self.pages)==1: # adding first page    
            self.defaultPage=pageName
            self.activePage.set(self.defaultPage)
            self.ChangePage()

    def RemovePage(self,pageName):
        if not pageName in self.pages.keys():
            raise 'Invalid TabPage Name'
        self.pages[pageName]['tab'].pack_forget()
        self.pages[pageName]['page'].grid_forget()
        self.pages[pageName]['tab'].destroy()
        self.pages[pageName]['page'].destroy()
        del(self.pages[pageName])
        # handle removing last remaining, or default, or active page
        if not self.pages: # removed last remaining page
            self.defaultPage=''
            return 
        if pageName==self.defaultPage: # set a new default page
            self.defaultPage=\
                self.tabBar.winfo_children()[0].button.cget('text')
        if pageName==self.GetActivePage(): # set a new active page 
            self.activePage.set(self.defaultPage)
        self.ChangePage()

if __name__ == '__main__':
    #test the dialog
    root=Tk()
    tabPage=TabPageSet(root,pageNames=['Foobar','Baz'])
    tabPage.pack(expand=TRUE,fill=BOTH)
    Label(tabPage.pages['Foobar']['page'],text='Foo',pady=20).pack()
    Label(tabPage.pages['Foobar']['page'],text='Bar',pady=20).pack()
    Label(tabPage.pages['Baz']['page'],text='Baz').pack()
    entryPgName=Entry(root)
    buttonAdd=Button(root,text='Add Page',
            command=lambda:tabPage.AddPage(entryPgName.get()))
    buttonRemove=Button(root,text='Remove Page',
            command=lambda:tabPage.RemovePage(entryPgName.get()))
    labelPgName=Label(root,text='name of page to add/remove:')
    buttonAdd.pack(padx=5,pady=5)
    buttonRemove.pack(padx=5,pady=5)
    labelPgName.pack(padx=5)
    entryPgName.pack(padx=5)
    root.mainloop()
        
