using System;
using System.ComponentModel;
using System.Threading.Tasks;
using Clio.XmlEngine;
using ff14bot;
using ff14bot.Helpers;
using ff14bot.Managers;
using ff14bot.NeoProfiles;
using TreeSharp;

namespace LlamaUtilities.OrderbotTags
{
    [XmlElement("LogFish")]
    public class LogFish : LLProfileBehavior
    {
        private bool _isDone;

        [XmlAttribute("ItemId")]
        public int FishId { get; set; }

        public override bool HighPriority => true;

        public override bool IsDone => _isDone;

        public LogFish() : base() { }

        protected override void OnStart()
        {
        }

        protected override void OnDone()
        {
        }

        protected override void OnResetCachedDone()
        {
            _isDone = false;
        }

        protected override Composite CreateBehavior()
        {
            return new ActionRunCoroutine(r => LogFishTask());
        }

        private Task LogFishTask()
        {
            Logging.WriteDiagnostic($"We have {ConditionParser.ItemCount((uint)FishId)} of {DataManager.GetItem((uint)FishId).CurrentLocaleName}");

            _isDone = true;
            return Task.CompletedTask;
        }
    }
}