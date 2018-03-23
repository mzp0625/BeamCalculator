from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from math import sqrt, pi
import json

from helpers import apology, isfloat, Cb_safe_div, Cap, None2Zero, contains

# Configure application
app = Flask(__name__)
app.secret_key = 'some_secret'

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///beams.db")


@app.route("/", methods = ["GET","POST"])
def index():
    """Homepage to prompt user to select shapes"""
    """Sends user to various URLs depending on the choice of steel section"""
    if request.method == "GET":
        return render_template("index.html")
    else: # POST
        if request.form.get("shapes") == "WF":
            return redirect("/WF")
        elif request.form.get("shapes") == "S":
            return redirect("/S")
        elif request.form.get("shapes") == "M":
            return redirect("/M")
        elif request.form.get("shapes") == "HP":
            return redirect("/HP")
        elif request.form.get("shapes") == "C":
            return redirect("/C")
        elif request.form.get("shapes") == "MC":
            return redirect("/MC")
        elif request.form.get("shapes") == "L":
            return redirect("/L")
        elif request.form.get("shapes") == "WT":
            return redirect("/WT")
        elif request.form.get("shapes") == "ST":
            return redirect("/ST")
        elif request.form.get("shapes") == "MT":
            return redirect("/MT")
        elif request.form.get("shapes") == "L2":
            return redirect("/L2")
        elif request.form.get("shapes") == "HSS":
            return redirect("/HSS")
        elif request.form.get("shapes") == "PIPE":
            return redirect("/PIPE")

# Pages of different shapes
@app.route("/WF", methods = ["GET","POST"])
def WF():
    WF_sections = db.execute("SELECT AISC_Manual_Label FROM properties \
                                    WHERE AISC_Manual_Label LIKE '%W%'\
                                    AND AISC_Manual_Label NOT LIKE '%WT%'")
    WF_list = []
    for i in range(len(WF_sections)):
        WF_list.append(WF_sections [i]['AISC_Manual_Label'])
    if request.method == "GET":
        return render_template("WF.html", WF_list = WF_list)
    elif request.method == "POST":
        # get section properties from beams.db
        A = round(float(db.execute("SELECT A FROM properties WHERE AISC_Manual_Label = :size",\
                        size = request.form.get("size"))[0]['A']),2)
        S_x = round(float(db.execute("SELECT S_x FROM properties WHERE AISC_Manual_Label = :size",\
                        size = request.form.get("size"))[0]['S_x']),2)
        S_y = round(float(db.execute("SELECT S_y FROM properties WHERE AISC_Manual_Label = :size",\
                        size = request.form.get("size"))[0]['S_y']),2)
        Z_x = round(float(db.execute("SELECT Z_x FROM properties WHERE AISC_Manual_Label = :size",\
                        size = request.form.get("size"))[0]['Z_x']),2)
        Z_y = round(float(db.execute("SELECT Z_y FROM properties WHERE AISC_Manual_Label = :size",\
                        size = request.form.get("size"))[0]['Z_y']),2)
        I_x = round(float(db.execute("SELECT I_x FROM properties WHERE AISC_Manual_Label = :size",\
                        size = request.form.get("size"))[0]['I_x']),2)
        I_y = round(float(db.execute("SELECT I_y FROM properties WHERE AISC_Manual_Label = :size",\
                        size = request.form.get("size"))[0]['I_y']),2)
        # Get name of WF beam
        name = db.execute("SELECT AISC_Manual_Label FROM properties WHERE AISC_Manual_Label = :size",\
                        size = request.form.get("size"))[0]['AISC_Manual_Label']
        # steel grade, E
        E = 29000.0
        # resistance factor
        phi = 0.90
        grade = request.form.get("grade")
        Fy = None
        if grade == "A36":
            Fy = 36
        elif grade == "A572":
            Fy = 50
        # axis of flexure
        axis = request.form.get("axis")
        # Unbraced length
        Lb = request.form.get("Lb")
        # M_A, M_B, M_C, Mu
        M_A = request.form.get("M_A")
        M_B = request.form.get("M_B")
        M_C = request.form.get("M_C")
        Mu = request.form.get("Mu")
        if (isfloat(Lb) == False or float(Lb) < 0) and Lb != '':
            flash("Enter a positive unbraced length!")
            return render_template("WF.html",WF_list = WF_list, \
                        A = A, S_x = S_x, S_y = S_y, Z_x = Z_x, \
                        Z_y = Z_y, I_x = I_x, I_y = I_y)
        elif (isfloat(M_A) == False or float(M_A) < 0) and M_A != '':
            flash("Enter a positive moment value!")
            return render_template("WF.html",WF_list = WF_list, \
                        A = A, S_x = S_x, S_y = S_y, Z_x = Z_x, \
                        Z_y = Z_y, I_x = I_x, I_y = I_y)
        elif (isfloat(M_B) == False or float(M_B) < 0) and M_B != '':
            flash("Enter a positive moment value!")
            return render_template("WF.html",WF_list = WF_list, \
                        A = A, S_x = S_x, S_y = S_y, Z_x = Z_x, \
                        Z_y = Z_y, I_x = I_x, I_y = I_y)
        elif (isfloat(M_C) == False or float(M_C) < 0) and M_C != '':
            flash("Enter a positive moment value!")
            return render_template("WF.html",WF_list = WF_list, \
                        A = A, S_x = S_x, S_y = S_y, Z_x = Z_x, \
                        Z_y = Z_y, I_x = I_x, I_y = I_y)
        elif (isfloat(Mu) == False or float(Mu) < 0) and Mu != '':
            flash("Enter a positive moment value!")
            return render_template("WF.html",WF_list = WF_list, \
                        A = A, S_x = S_x, S_y = S_y, Z_x = Z_x, \
                        Z_y = Z_y, I_x = I_x, I_y = I_y)
        elif Lb == '' or M_A == '' or M_B == '' or M_C == '' or Mu == '':
            return render_template("WF.html",WF_list = WF_list, \
                        A = A, S_x = S_x, S_y = S_y, Z_x = Z_x, \
                        Z_y = Z_y, I_x = I_x, I_y = I_y)
        else:
            # additional properties from beams.db
            b_f = float(db.execute("SELECT b_f FROM properties WHERE AISC_Manual_Label = :size",\
                        size = request.form.get("size"))[0]['b_f'])
            t_f = float(db.execute("SELECT t_flange FROM properties WHERE AISC_Manual_Label = :size",\
                        size = request.form.get("size"))[0]['t_flange'])
            r_ts = float(db.execute("SELECT r_ts FROM properties WHERE AISC_Manual_Label = :size",\
                        size = request.form.get("size"))[0]['r_ts'])
            J = float(db.execute("SELECT J FROM properties WHERE AISC_Manual_Label = :size",\
                        size = request.form.get("size"))[0]['J'])
            h_o = float(db.execute("SELECT h_o FROM properties WHERE AISC_Manual_Label = :size",\
                        size = request.form.get("size"))[0]['h_o'])
            C_w = float(db.execute("SELECT C_w FROM properties WHERE AISC_Manual_Label = :size",\
                        size = request.form.get("size"))[0]['C_w'])
            r_y = float(db.execute("SELECT r_y FROM properties WHERE AISC_Manual_Label = :size",\
                        size = request.form.get("size"))[0]['r_y'])
            k_des = float(db.execute("SELECT k_des FROM properties WHERE AISC_Manual_Label = :size",\
                        size = request.form.get("size"))[0]['k_des'])
            d = float(db.execute("SELECT d FROM properties WHERE AISC_Manual_Label = :size",\
                        size = request.form.get("size"))[0]['d'])
            t_w = float(db.execute("SELECT t_w FROM properties WHERE AISC_Manual_Label = :size",\
                        size = request.form.get("size"))[0]['t_w'])
            h = d - 2*k_des
            # Initialize failure mode
            fail_mode = None
            # c = 1 for WF beams
            c = 1.0
            # Calculate Lp, Lr, Cb
            Lb, M_A, M_B, M_C, Mu = 12*float(Lb), 12*float(M_A), 12*float(M_B), 12*float(M_C), 12*float(Mu)
            Cb = Cb_safe_div(12.5*Mu ,2.5*Mu + 3*M_A + 4*M_B + 3*M_C)
            Lp = 1.76*r_y*sqrt(E/Fy)
            Lr = 1.95*r_ts*(E/(0.7*Fy)) * sqrt(J*c/(S_x*h_o) + sqrt(J*c/pow((S_x*h_o),2) + 6.76*pow((0.7*Fy/E),2)))
            # Compactness
            kc = Cap(4/sqrt(h/t_w),0.35,0.76)
            lambd = b_f/(2*t_f)
            lambd_pf = 0.38 * sqrt(E/Fy)
            lambd_rf = 1.0 * sqrt(E/Fy)
            # initialize results as None
            M_factored, DCR = None, None
            if axis == 'X_axis':
                axis = "X - axis"
                # check compactness
                if b_f/(2*t_f) < 0.38 * sqrt(E/Fy) and h/t_w < 3.76 * sqrt(E/Fy): # Fully compact
                    # plastic moment
                    Mp = Fy * Z_x
                    if Lb < Lp:
                        Mn = Mp
                        fail_mode = "Flexural Yielding"
                    # LTB for Lp<Lb<Lr
                    elif Lb > Lp and Lb < Lr:
                        Mn =  min(Mp - (Mp - 0.7*Fy*S_x) * ((Lb - Lp)/(Lr - Lp)), Mp)
                        fail_mode = "Lateral-Torsional Buckling"
                    # LTB for Lb<Lr
                    elif Lb > Lr:
                        Fcr = Cb*pow(pi,2)*E/pow((Lb/r_ts),2) * sqrt(1 + 0.078*J*c/(S_x*h_o)*pow((Lb/r_ts),2))
                        Mn= min(Fcr*S_x, Mp)
                        fail_mode = "Lateral-Torsional Buckling"
                    # phi*Mn [k-ft]
                    M_factored = round(phi * Mn / 12,2)
                    DCR = round(Mu/12/M_factored,2)
                    Mode = "The failure mode of " + " ASTM " + grade + ' ' + name + " bent about " + axis + " is " + fail_mode
                    return render_template("WF.html",WF_list = WF_list, \
                        A = A, S_x = S_x, S_y = S_y, Z_x = Z_x, \
                        Z_y = Z_y, I_x = I_x, I_y = I_y, M_factored = M_factored,\
                        DCR = DCR, Mode = Mode)
                elif h/t_w < 3.76 * sqrt(E/Fy) and b_f/(2*t_f) > 0.38 * sqrt(E/Fy): # Web compact
                    M_LTB = None
                # LTB capacity
                    # plastic moment
                    Mp = Fy * Z_x
                    if Lb < Lp:
                        M_LTB = Mp
                    # LTB for Lp<Lb<Lr
                    elif Lb > Lp and Lb < Lr:
                        M_LTB =  min(Mp - (Mp - 0.7*Fy*S_x) * ((Lb - Lp)/(Lr - Lp)), Mp)
                    # LTB for Lb<Lr
                    elif Lb > Lr:
                        M_LTB= min(Fcr*S_x, Mp)
                # Compression flange local buckling
                    if lambd < lambd_pf: # Compact
                        Mn = Mp
                    elif lambd < lambd_rf and lambd > lambd_pf: # Non-Compact
                        Mn = Mp - (Mp-0.7*Fy*S_x)*(lambd - lambd_pf) / (lambd_rf - lambd_pf)
                    elif lambd > lambd_pf:
                        Mn = 0.9*E*kc*S_x/pow(lambd,2) # Slender
                    M_factored = round (phi * min(Mp, M_LTB , Mn)/12 ,2)
                    DCR = round(Mu/12/M_factored,2)
                    # find failure mode
                    if Mp == min(Mp, M_LTB, Mn):
                        fail_mode = "Flexural Yielding"
                    elif M_LTB == min(Mp, M_LTB, Mn):
                        fail_mode = "Lateral-Torsional Buckling"
                    elif Mn == min(Mp, M_LTB, Mn):
                        fail_mode = "Compression Flange Local Buckling"
                    Mode = "The failure mode of " + " ASTM " + grade + ' ' + name + " bent about " + axis + " is " + fail_mode
                    return render_template("WF.html",WF_list = WF_list, \
                        A = A, S_x = S_x, S_y = S_y, Z_x = Z_x, \
                        Z_y = Z_y, I_x = I_x, I_y = I_y, M_factored = M_factored,\
                        DCR = DCR, Mode = Mode)
                else : # web slender, also used conservatively to design for non-compact web
                # Failure modes
                    # Compression flange yielding
                    h_c = d/2 - t_f
                    a_w = h_c*t_w/(b_f*t_f)
                    Rpg = 1-a_w/(1200+200*a_w)*(h_c/t_w-5.7*sqrt(E/Fy))
                    Rpg = Cap(Rpg, Rpg, 1.0)
                    r_t = b_f/sqrt(12*(1 + a_w/6))
                    M_CFY = Rpg*Fy*S_x
                    # Lateral torsional buckling
                    if Lb < Lp:
                        M_LTB = M_CFY
                    elif Lb > Lp and Lb < Lr:
                        Fcr = Cb*(Fy - 0.3*Fy*(Lb - Lp)/(Lr - Lp))
                        Fcr = Cap(Fcr, Fcr, Fy)
                    elif Lb > Lr:
                        Fcr = Cb*pow(pi,2)*E/pow((Lb/r_t),2)
                        Fcr = Cap(Fcr, Fcr, Fy)
                    M_LTB = Rpg*Fcr*S_x
                    if lambd < lambd_pf: # Compact
                        Fcr = Fy
                    # Compression Flange Local Buckling
                    elif lambd < lambd_rf and lambd > lambd_pf: # Non-compact
                        Fcr = Fy - (0.3*Fy)*(lambd - lambd_pf)/(lambd_rf - lambd_pf)
                    elif lambd > lambd_rf: # Slender
                        Fcr = 0.9*E*kc/pow((b_f/2*t_f),2)
                    M_CFLB = Rpg*Fcr*S_x
                    # Tension Flange Yielding
                    # Does not apply for standard AISC W shapes
                    M_factored = round(phi * min(M_CFY, M_LTB, M_CFLB) / 12, 2)
                    DCR = round(Mu/12/M_factored,2)
                    # find failure mode
                    if M_CFY == min(M_CFY, M_LTB, M_CFLB):
                        fail_mode = "Compression Flange Yielding"
                    elif M_LTB == min(M_CFY, M_LTB, M_CFLB):
                        fail_mode = "Lateral-Torsional Buckling"
                    elif M_CFLB == min(M_CFY, M_LTB, M_CFLB):
                        fail_mode = "Compression Flange Local Buckling"
                    Mode = "The failure mode of " + " ASTM " + grade + ' ' + name + " bent about " + axis + " is " + fail_mode
                    return render_template("WF.html",WF_list = WF_list, \
                        A = A, S_x = S_x, S_y = S_y, Z_x = Z_x, \
                        Z_y = Z_y, I_x = I_x, I_y = I_y, M_factored = M_factored,\
                        DCR = DCR, Mode = Mode)
            elif axis == 'Y_axis':
                axis = "Y - axis"
                # Get properties required

                # Yielding
                Mp = Fy*Z_y
                fail_mode = "Flexural Yielding"
                # Flange Local Buckling
                M_FLB = None
                if lambd < lambd_pf: # Compact
                    M_FLB = Mp
                    fail_mode = "Flexural Yielding"
                elif lambd < lambd_rf and lambd > lambd_pf: # Non-compact
                    M_FLB = Mp - (Mp - 0.7*Fy*S_y)*(lambd - lambd_pf)/(lambd_rf - lambd_pf)
                    fail_mode = "Flange Local Buckling"
                elif lambd > lambd_rf:
                    Fcr = 0.69*E/pow((b_f/2/t_f),2)
                    M_FLB = Fcr * S_y
                    fail_mode = "Flange Local Buckling"
                M_factored = round(phi * min(Mp, M_FLB)/12, 2)
                DCR = round(Mu/12/M_factored, 2)
                Mode = "The failure mode of " + " ASTM " + grade + ' ' + name + " bent about " + axis + " is " + fail_mode
                return render_template("WF.html",WF_list = WF_list, \
                        A = A, S_x = S_x, S_y = S_y, Z_x = Z_x, \
                        Z_y = Z_y, I_x = I_x, I_y = I_y, M_factored = M_factored,\
                        DCR = DCR, Mode = Mode)

@app.route("/S", methods = ["GET","POST"])
def S():

    return apology("Beam calculator for this shape yet to be implemented!")

@app.route("/M", methods = ["GET","POST"])
def M():

    return apology("Beam calculator for this shape yet to be implemented!")

@app.route("/HP", methods = ["GET","POST"])
def HP():

    return apology("Beam calculator for this shape yet to be implemented!")

@app.route("/C", methods = ["GET","POST"])
def C():

    return apology("Beam calculator for this shape yet to be implemented!")

@app.route("/MC", methods = ["GET","POST"])
def MC():

    return apology("Beam calculator for this shape yet to be implemented!")

@app.route("/L", methods = ["GET","POST"])
def L():

    return apology("Beam calculator for this shape yet to be implemented!")

@app.route("/WT", methods = ["GET","POST"])
def WT():

    return apology("Beam calculator for this shape yet to be implemented!")

@app.route("/ST", methods = ["GET","POST"])
def ST():

    return apology("Beam calculator for this shape yet to be implemented!")

@app.route("/MT", methods = ["GET","POST"])
def MT():

    return apology("Beam calculator for this shape yet to be implemented!")

@app.route("/L2", methods = ["GET","POST"])
def L2():

    return apology("Beam calculator for this shape yet to be implemented!")

@app.route("/HSS", methods = ["GET","POST"])
def HSS():
    """Create a list of all rectangular and square HSS"""
    HSS_sections = db.execute("SELECT AISC_Manual_Label FROM properties \
                                WHERE AISC_Manual_Label LIKE '%HSS%'")
    HSS_list = []
    for i in range(len(HSS_sections)):
        name = HSS_sections[i]['AISC_Manual_Label']
        if name.count('X') == 2: # Square or rectangular HSS
            HSS_list.append(name)

    if request.method == "GET":
        return render_template("HSS.html", HSS_list = HSS_list)

    elif request.method == "POST":
            # get section properties from beams.db
        A = round(float(db.execute("SELECT A FROM properties WHERE AISC_Manual_Label = :size",\
                        size = request.form.get("size"))[0]['A']),2)
        S_x = round(float(db.execute("SELECT S_x FROM properties WHERE AISC_Manual_Label = :size",\
                        size = request.form.get("size"))[0]['S_x']),2)
        S_y = round(float(db.execute("SELECT S_y FROM properties WHERE AISC_Manual_Label = :size",\
                        size = request.form.get("size"))[0]['S_y']),2)
        Z_x = round(float(db.execute("SELECT Z_x FROM properties WHERE AISC_Manual_Label = :size",\
                        size = request.form.get("size"))[0]['Z_x']),2)
        Z_y = round(float(db.execute("SELECT Z_y FROM properties WHERE AISC_Manual_Label = :size",\
                        size = request.form.get("size"))[0]['Z_y']),2)
        I_x = round(float(db.execute("SELECT I_x FROM properties WHERE AISC_Manual_Label = :size",\
                        size = request.form.get("size"))[0]['I_x']),2)
        I_y = round(float(db.execute("SELECT I_y FROM properties WHERE AISC_Manual_Label = :size",\
                        size = request.form.get("size"))[0]['I_y']),2)
        OD = round(float(db.execute("SELECT OD FROM properties WHERE AISC_Manual_Label = :size",\
                        size = request.form.get("size"))[0]['OD']),2)
        t = round(float(db.execute("SELECT t_des FROM properties WHERE AISC_Manual_Label = :size",\
                        size = request.form.get("size"))[0]['t_des']),2)
        # Get name of WF beam
        name = db.execute("SELECT AISC_Manual_Label FROM properties WHERE AISC_Manual_Label = :size",\
                        size = request.form.get("size"))[0]['AISC_Manual_Label']
        # steel grade, E
        E = 29000.0
        # resistance factor
        phi = 0.90
        # Fy
        Fy = 46
        # axis of flexure
        axis = request.form.get("axis")
        fail_mode = None
        Mu = None2Zero(request.form.get("Mu"))
        # Check if input for Mu is valid
        if isfloat(Mu) == False or float(Mu) < 0:
            flash("Enter a positive moment value!")
            return render_template("HSS.html", HSS_list = HSS_list, A = A, S_x = S_x, S_y = S_y,\
                                    Z_x = Z_x, Z_y = Z_y, I_x = I_x, I_y = I_y)
        else:
            Mu = float(Mu)
            if axis == 'X_axis':
                Z = Z_x
                S = S_x
                lambd_flange = b/t
                lambd_web = h/t
                # Limit State of Yielding
                Mp = Fy*Z
                M_FLB = Mp
                M_WLB = Mp
                # Limit State of Flange Local Buckling
                if lambd_flange < 1.12*sqrt(E/Fy): # Compact
                    M_FLB = Mp
                elif lambd_flange > 1.12*sqrt(E/Fy) and lambd_flange < 1.4*sqrt(E/Fy): # Non Compact
                    M_FLB = Mp - (Mp-Fy*S)*(3.57*b/t*sqrt(Fy/E)-4.0)
                    M_FLB = Cap(M_FLB, M_FLB, Mp)
                elif lambd_flange > 1.4*sqrt(E/Fy): # Slender
                    b_e = 1.92*t*sqrt(E/Fy)*(1 - 0.38/(b/t)*sqrt(E/Fy))
                    b_e = Cap(b_e, b_e, b)
                    S_e = b_e/b*S
                    M_FLB = Fy*S_e
                # Limit State of Web Local Buckling
                if lambd_web < 2.42*sqrt(E/Fy):  # Compact
                    M_WLB = Mp
                elif lambd_web > 2.42*sqrt(E/Fy) and lambd_web < 5.70*sqrt(E/Fy): # Non-compact
                    M_WLB = Mp - (Mp - Fy*S)*(0.305*h/t*sqrt(Fy/E) - 0.738)
                    M_WLB = Cap(M_WLB, M_WLB, Mp)
                if Mp <= M_FLB and Mp <= M_WLB:
                    fail_mode = "Flexural Yielding"
                elif M_FLB < Mp and M_FLB < M_WLB:
                    fail_mode = "Flange Local Buckling"
                elif M_WLB < Mp and M_WLB < M_FLB:
                    fail_mode = "Web Local Buckling"
                M_factored = round(phi*min(Mp, M_FLB, M_WLB)/12,2)
                DCR = round(Mu/M_factored,2)
                Mode = "The failure mode of " + name + " bent about X-axis is " + fail_mode
            elif axis == 'Y_axis':
                Z = Z_y
                S = S_y
                lambd_flange = h/t
                lambd_web = b/t
                # Limit State of Yielding
                Mp = Fy*Z
                M_FLB = Mp
                M_WLB = Mp
                # Limit State of Flange Local Buckling
                if lambd_flange < 1.12*sqrt(E/Fy): # Compact
                    M_FLB = Mp
                elif lambd_flange > 1.12*sqrt(E/Fy) and lambd < 1.4*sqrt(E/Fy): # Non Compact
                    M_FLB = Mp - (Mp-Fy*S)*(3.57*b/t*sqrt(Fy/E)-4.0)
                    M_FLB = Cap(M_FLB, M_FLB, Mp)
                elif lambd_flange > 1.4*sqrt(E/Fy): # Slender
                    b_e = 1.92*t*sqrt(E/Fy)*(1 - 0.38/(b/t)*sqrt(E/Fy))
                    b_e = Cap(b_e, b_e, b)
                    S_e = b_e/b*S
                    M_FLB = Fy*S_e
                # Limit State of Web Local Buckling
                if lambd_web < 2.42*sqrt(E/Fy):  # Compact
                    M_WLB = Mp
                elif lambd_web > 2.42*sqrt(E/Fy) and lambd_web < 5.70*sqrt(E/y): # Non-compact
                    M_WLB = Mp - (Mp - Fy*S)*(0.305*h/t*sqrt(Fy/E) - 0.738)
                    M_WLB = Cap(M_WLB, M_WLB, Mp)
                if Mp <= M_FLB and Mp <= M_WLB:
                    fail_mode = "Flexural Yielding"
                elif M_FLB < Mp and M_FLB < M_WLB:
                    fail_mpde = "Flange Local Buckling"
                elif M_WLB < Mp and M_WLB < M_FLB:
                    fail_mode = "Web Local Buckling"
                M_factored = round(phi*min(Mp, M_FLB, M_WLB)/12,2)
                DCR = round(Mu/M_factored,2)
                Mode = "The failure mode of " + name + " bent about Y-axis is " + fail_mode
            return render_template("HSS.html", HSS_list = HSS_list, A = A, S_x = S_x, S_y = S_y,\
                                    Z_x = Z_x, Z_y = Z_y, I_x = I_x, I_y = I_y, Mode = Mode, \
                                    M_factored = M_factored, DCR = DCR)


@app.route("/PIPE", methods = ["GET","POST"])
def PIPE():
    """Create a list of all round HSS and PIPES"""
    PIPE_sections = db.execute("SELECT AISC_Manual_Label FROM properties \
                                WHERE AISC_Manual_Label LIKE '%PIPE%'")
    HSS_sections = db.execute("SELECT AISC_Manual_Label FROM properties \
                                WHERE AISC_Manual_Label LIKE '%HSS%'")
    PIPE_list = []
    for i in range(len(HSS_sections)):
        name = HSS_sections[i]['AISC_Manual_Label']
        if name.count('X') == 1: # Square or rectangular HSS
            PIPE_list.append(name)
    for i in range(len(PIPE_sections)):
        PIPE_list.append(PIPE_sections[i]['AISC_Manual_Label'])

    if request.method == "GET":
        return render_template("PIPE.html", PIPE_list = PIPE_list)

    elif request.method =="POST":
        A = round(float(db.execute("SELECT A FROM properties WHERE AISC_Manual_Label = :size",\
                        size = request.form.get("size"))[0]['A']),2)
        S = round(float(db.execute("SELECT S_x FROM properties WHERE AISC_Manual_Label = :size",\
                        size = request.form.get("size"))[0]['S_x']),2)
        Z = round(float(db.execute("SELECT Z_x FROM properties WHERE AISC_Manual_Label = :size",\
                        size = request.form.get("size"))[0]['Z_x']),2)
        I = round(float(db.execute("SELECT I_x FROM properties WHERE AISC_Manual_Label = :size",\
                        size = request.form.get("size"))[0]['I_x']),2)
        OD = round(float(db.execute("SELECT OD FROM properties WHERE AISC_Manual_Label = :size",\
                        size = request.form.get("size"))[0]['OD']),2)
        t = round(float(db.execute("SELECT t_des FROM properties WHERE AISC_Manual_Label = :size",\
                        size = request.form.get("size"))[0]['t_des']),2)
        name = db.execute("SELECT AISC_Manual_Label FROM properties WHERE AISC_Manual_Label = :size",\
                        size = request.form.get("size"))[0]['AISC_Manual_Label']
        Mu = None2Zero(request.form.get("Mu"))

        shape, Fy, E, fail_mode, M_factored, DCR, Mode, phi = None, None, 29000, None, None, None, None, 0.90
        if contains('HSS', name):
            shape = "HSS"
            Fy = 46

            if isfloat(Mu) == False or float(Mu) < 0:
                flash("Enter a positive moment value!")
                return render_template("PIPE.html", PIPE_list = PIPE_list, A = A, S = S, Z = Z, I = I, Fy = Fy)
            else:
                Mu = float(Mu)
                # Yielding
                Mp = Fy*Z
                fail_mode = "yielding"
                # Local Buckling
                # Compact
                if OD/t < 0.07*E/Fy:# Compact
                    M_LB = Mp
                    fail_mode = "yielding"
                elif OD/t > 0.07*E/Fy and OD/t < 0.31*E/Fy: # Non-Compact
                    M_LB = (0.021*E/(OD/t) + Fy)*S
                    fail_mode = "local buckling"
                elif OD/t > 0.31 * E/Fy: # Slender
                    F_cr = 0.33*E/(OD/t)
                    M_LB = F_cr * S
                    fail_mode = "local buckling"
                M_factored = round(phi*min(Mp, M_LB)/12,2)
                DCR = round(Mu/M_factored,2)
                Mode = "The failure mode of " + name + " is " + fail_mode
                return render_template("PIPE.html", PIPE_list = PIPE_list, A = A, S = S, Z = Z, I = I, Fy = Fy,\
                                        M_factored = M_factored, DCR = DCR, Mode = Mode)

        elif contains('PIPE', name):
            shape = "PIPE"
            Fy = 36

            if isfloat(Mu) == False or float(Mu) < 0:
                flash("Enter a positive moment value!")
                return render_template("PIPE.html", PIPE_list = PIPE_list, A = A, S = S, Z = Z, I = I, Fy = Fy)
            else:
                Mu = float(Mu)
                # Yielding
                Mp = Fy*Z
                fail_mode = "flexural yielding"
                # Local Buckling
                # Compact
                if OD/t < 0.07*E/Fy:# Compact
                    M_LB = Mp
                    fail_mode = "flexural yielding"
                elif OD/t > 0.07*E/Fy and OD/t < 0.31*E/Fy: # Non-Compact
                    M_LB = (0.021*E/(OD/t) + Fy)*S
                    fail_mode = "local buckling"
                elif OD/t > 0.31 * E/Fy: # Slender
                    F_cr = 0.33*E/(OD/t)
                    M_LB = F_cr * S
                    fail_mode = "local buckling"
                M_factored = round(phi*min(Mp, M_LB)/12,2)
                DCR = round(Mu/M_factored,2)
                Mode = "The failure mode of " + name + " is " + fail_mode
                return render_template("PIPE.html", PIPE_list = PIPE_list, A = A, S = S, Z = Z, I = I, Fy = Fy,\
                                        M_factored = M_factored, DCR = DCR, Mode = Mode)
def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)