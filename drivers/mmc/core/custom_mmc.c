/******************* kernel\drivers\mmc\core\custom_mmc.c ************************
    ��    ��: �� �� 
    ��    ��: ��ʼ�汾   1.0
    ��    ��: ���ļ��Զ�����,�벻Ҫ�ֶ��޸�      
******************************************************************/
//ͷ�ļ�����
#include <linux/err.h>
#include <linux/slab.h>
#include <linux/stat.h>

#include <linux/mmc/host.h>
#include <linux/mmc/card.h>
#include <linux/mmc/mmc.h>

#include "core.h"
#include "bus.h"
#include "mmc_ops.h"
#include "sd_ops.h"

#include "custom_mmc.h"

//��̬��������

//��̬��������

//ȫ�ֱ�������

static const EMMC_INFO CKT_EMMC[3] =
{
	{
		{0x45010053,0x454d3038,0x47000000,0x00000000},
		"sandiskSDIN8DE1-8GB"
	},
	{
		{0x11010030,0x31364739,0x32000000,0x00000000},
		"THGBMAG7A2JBAIR-16G"
	},
	{
		{0x11010030,0x33324739,0x36000000,0x00000000},
		"THGBMAG8A4JBA4R-32G"
	},
	{
		{0x90014A48,0x34473164,0x04000000,0x00000000},
		"H9TP32A8JDACPR_KGM"
	},
	{
		{0x1501004B,0x3758564D,0x42000000,0x00000000},
		"KMK7X000VM_B314"
	},
};

/******************* ������: GetEMMCName **********************
    ��������: ����raw_id�ĶԱ��ҵ���Ӧ��emmc������
    ��������: 
        card :mmc_card,���а�����raw_id
    ��������: char * emmc������
    ��    ��: 
****************************************************************/
const char *GetEMMCName(const struct mmc_card const *card)
{	
	int i;
	const static char * unknown="unknown";
	for(i=0;i<sizeof(CKT_EMMC)/sizeof(CKT_EMMC[0]);i++ )
	{
		if(
			(CKT_EMMC[i].raw_cid[0] == card->raw_cid[0])
			&&(CKT_EMMC[i].raw_cid[1] == card->raw_cid[1])
			&&((CKT_EMMC[i].raw_cid[2]&0xff000000)==(card->raw_cid[2]&0xff000000))
		  )
		{
			return CKT_EMMC[i].name;
		}
	}
	return unknown;
}


