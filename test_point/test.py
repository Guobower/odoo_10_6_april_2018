<xpath expr="//page[@name='personal_information']/group" position="before">
<xpath expr="sheet/notebook" position="after">
                        <field name="notes" placeholder="Other Information ..." colspan="4"/>
                </xpath>
<field name="context">{'search_default_todo':1, 'show_purchase': True,'default_ttype': 'fabric','default_yarnt_fabricf':1}}</field>
# tree ki field ko field sa replace
          <xpath expr="//field[@name ='order_line']/tree/field[@name ='product_id']" position="replace">
                <field name="product_id" domain="[('ttype', '=', parent.ttype)]"/>
            </xpath>