import os
def loshmarKA():
	if os.getenv("VCAP_SERVICES") is not None:
		print "Started assignment"
		field1 = "\"Activity\""
		field2 = "\"Start\""
		field3 = "\"Finish\""
		field4 = "\"Material\""
		###XXXXXXXXXXXXXXXX        MB51     XXXXXXXXXXXXXXXXXXX'
		field4 = "\"Material\""
		field5 = "\"Material Description\""
		field6 = "\"Plnt\""
		field7 = "\"SLoc\""
		field8 = "\"MvT\""
		field9 = "\"Movement Type Text\""
		field10 = "\"Mat. Doc.\""
		field11 = "\"Item1\""
		field12 = "\"Pstng Date\""
		field13 = "\"Qty in UnE\""
		field14 = "\"Amount LC\""
		field15 = "\"PO\""
		field16 = "\"Item\""
		field17 = "\"Order\""
		field18 = "\"Crcy\""
		###XXXXXXXXXXXXXXXXXX   Coois Headers XXXXXXXXXXXXXXXXXXX'
		field19 = "\"Order\""
		field20 = "\"Material\""
		field21 = "\"MRP ctrlr\""
		field22 = "\"Order Type\""
		field23 = "\"Target qty\""
		field24 = "\"Unit\""
		field25 = "\"Bsc start\""
		field26 = "\"Basic fin.\""
		field27 = "\"Material description\""
		field28 = "\"System Status\""
		field29 = "\"Firming\""
		field30 = "\"Plant\""
		###'XXXXXXXXXXXX Coois Operations XXXXXXXXXXXXXXXXXXX'
		field31 = "\"Order\""
		field32 = "\"Oper./Act.\""
		field33 = "\"Work cntr.\""
		field34 = "\"Operation short text\""
		field35 = "\"Op. Qty\""
		field36 = "\"Act/Op.UoM\""
		field37 = "\"Act. start\""
		field38 = "\"Act.finish\""
		field39 = "\"LatestFin.\""
		field40 = "\"System Status\""
		field41 = "\"Yield\""
		field42 = "\"Std Value\""
		field43 = "\"Conf. act.\""
		field44 = "\"Rework\""
		field45 = "\"Plnt\""
		field46 = "\"Processing\""
		field47 = "\"Text key\""
		
		###'XXXXXXXXXXXX       Zp03       XXXXXXXXXXXXXXXXXXX'
		field48 = "\"Work_Center\""
		field49 = "\"Plant\""
		field50 = "\"Date\""
		field51 = "\"Time\""
		field52 = "\"N/P\""
		field53 = "\"Order\""
		field54 = "\"Operation No\""
		field55 = "\"Emp\""
		field56 = "\"Setup\""
		field57 = "\"Unit\""
		field58 = "\"Machine\""
		field59 = "\"Unit1\""
		field60 = "\"Labor\""
		field61 = "\"Unit2\""
		field62 = "\"Rework\""
		field63 = "\"Unit3\""
		field64 = "\"Qty\""
		field65 = "\"BUn\""
		field66 = "\"F\""
		field67 = "\"Op_STD_Lab\""
		##'XXXXXXXXXXX     CM01 Details        XXXXXXXXXXXXXXXX'
		field68 = "\"Day\""
		field69 = "\"Material\""
		field70 = "\"Material description\""
		field71 = "\"Order\""
		field72 = "\"Op.\""
		field73 = "\"Stat\""
		field74 = "\" PgRqmtQty\""
		field75 = "\"  TgtSetup\""
		field76 = "\"  TrgtProc\""
		field77 = "\"Sales ord.\""
		field78 = "\"LatestFin.\""
		field79 = "\"MRP\""
		field80 = "\"Work Ctr\""
		field81 = "\"Plnt\""
		field82 = "\"Operation text\""
		field83 = "\"Finish\""
		
		##XXXXXXXXXXXXXXXXXX        NCR_data           XXXXXXXXXXXXXXXXXXXX
		field84 = "\"Pending\""
		field85 = "\"NCR#\""
		field86 = "\"Part# 2\""
		field87 = "\"Pending Stage\""
		field88 = "\"Owner Inits\""
		field89 = "\"Logged Date 2\""
		field90 = "\"Cell\""
		field91 = "\"CCC?\""
		field95="\"Pull_Date\"" 
		fieldPLL = "\"Pull_Date\"";
		##XXXXXXXXXXXXXXXXXX        META_data           XXXXXXXXXXXXXXXXXXXX
		field92 = "\"Table\""
		field93 = "\"Feedback_Type\""
		field94 = "\"Datetime\""
		field96 = "\"Status_Code\""
			
		##XXXXXXXXXXXXXXXXXX        CM01_Extra_data           XXXXXXXXXXXXXXXXXXXX
		field97 = "\"Available_cap\""
		field98 = "\" Requirements\""
		print "Finished assignment"
	else:
		print "Started assignment"
		field2s = "Material Description"
		##XXXXXXXXXXXXXXXXXX        NCR_fields          XXXXXXXXXXXXXXXXXXXX
		field84 = "Pending"
		field85 = "NCR#"
		field86 = "Part# 2"
		field87 = "Pending Stage"
		field88 = "Owner Inits"
		field89 = "Logged Date 2"
		field90 = "Cell"
		field91 = "CCC?"
		
		##XXXXXXXXXXXXXXXXXX        META_data           XXXXXXXXXXXXXXXXXXXX
		field92 = "Table"
		field93 = "Feedback_Type"
		field94 = "Datetime"
		field96 = "Status_Code"
		
		##XXXXXXXXXXXXXXXXXX        CM01_Extra_data           XXXXXXXXXXXXXXXXXXXX
		field97 = "'Available capacit'"
		field98 = "' Requirements'"
		
		##'XXXXXXXXXXX     ZP03 fields        XXXXXXXXXXXXXXXX'
		field48="'Work_Center'"
		field49="'Plant'"
		field50="'Date'"
		field51="'Time'"
		field52="'N/P'"
		field53="'Order'"
		field54="'Operation No'"
		field55="'Emp'"
		field56="'Setup'"
		field57="'Unit1'"
		field58="'Machine'"
		field59="'Unit2'"
		field60="'Labor'"
		field61="'Unit3'"
		field62="'Rework'"
		field63="'Unit4'"
		field64="'Qty'"
		field65="'BUn'"
		field66="'F'"
		field67="'Op_Std_Labor'"
		##'XXXXXXXXXXx       Coois_H         xXXXXXXXXXXXX'
		field19="'Order'"
		field20="'Material'"
		field21="'MRP ctrlr'"
		field22="'Order Type'"
		field23="'Target qty'"
		field24="'Unit'"
		field25="'Bsc start'"
		field26="'Basic fin.'"
		field27="'Material description'"
		field28="'System Status'"
		field29="'Firming'"
		field30="'Plant'"
		##'XXXXXXXXXXXXX       Coois Ops Fields    XXXXXXXXXXXXXXXXXX'
		field31="'Order'"
		field32="'Oper./Act.'"
		field33="'Work cntr.'"
		field34="'Opr. short text'"
		field35="'Op. Qty'"
		field36="'Act/Op.UoM'"
		field37="'Act. start'"
		field38="'Act.finish'"
		field39="'LatestFin.'"
		field40="'System Status'"
		field41="' Yield'"
		field42="'Std Value'"
		field43="'Conf. act.'"
		field44="'Rework'"
		field45="'Plnt'"
		field46="' Processing'"
		field47="'Text key'"
		
		##'XXXXXXXXXXXX       MB51 fields    XXXXXXXXXXXXXXXXXX'
		field4="'Material'"
		field5="'Material Description'"
		field6="'Plnt'"
		field7="'SLoc'"
		field8="'MvT'"
		field9="'Movement Type Text'"
		field10="'Mat. Doc.'"
		field11="'Item'"
		field12="'Pstng Date'"
		field13="'Qty in UnE'"
		field14="'  Amount LC'"
		field15="'PO'"
		field16="'Item1'"
		field17="'Order'"
		field18="'Crcy'"
		###XXXXXXXx          CM01 Fields at phppgadmin      XXXXXXXXXXXXXXXXXXX
		field68 = "'Day'"
		field69 = "'Material'"
		field70 = "'Material description'"
		field71 = "'Order'"
		field72 = "'Op.'"
		field73 = "'Stat'"
		field74 = "' PgRqmtQty'"
		field75 = "' TgtSetup'"
		field76 = "' TrgtProc'"
		field77 = "'Sales ord.'"
		field78 = "'LatestFin.'"
		field79 = "'MRP'"
		field80 = "'Work Ctr'"
		field81 = "'Plnt'"
		field82 = "'Operation text'"
		field83 = "'Finish'"
		print "Finished assignment"